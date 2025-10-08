from typing import Dict, Tuple, Any, Iterable, Optional, List
import networkx as nx

def _pairwise(seq: List[str]):
    for i in range(len(seq) - 1):
        yield seq[i], seq[i + 1]

def _edge_ids_on_path(G: nx.Graph, node_path: Optional[List[str]]) -> Optional[List[Optional[Any]]]:
    """Return [eid1, eid2, ...] along the node_path; None if no path or eid missing."""
    if not node_path:
        return None
    is_multi = isinstance(G, (nx.MultiGraph, nx.MultiDiGraph))
    eids: List[Optional[Any]] = []
    for u, v in _pairwise(node_path):
        eid = None
        if is_multi:
            data_dict = G.get_edge_data(u, v)  # {key: attrdict}
            if data_dict:
                _, d = next(iter(data_dict.items()))
                eid = d.get("eid")
        else:
            d = G.get_edge_data(u, v)
            if d:
                eid = d.get("eid")
        eids.append(eid)
    return eids

def _node_edge_chain(G: nx.Graph, node_path: Optional[List[str]]) -> Optional[List[Any]]:
    """['n1','n3','n6'] -> ['n1', eid(n1,n3), 'n3', eid(n3,n6), 'n6'] (uses 'eid', falls back to 'u->v')."""
    if not node_path:
        return None
    chain: List[Any] = [node_path[0]]
    is_multi = isinstance(G, (nx.MultiGraph, nx.MultiDiGraph))
    for u, v in _pairwise(node_path):
        eid = None
        if is_multi:
            data_dict = G.get_edge_data(u, v)
            if data_dict:
                _, d = next(iter(data_dict.items()))
                eid = d.get("eid")
        else:
            d = G.get_edge_data(u, v)
            if d:
                eid = d.get("eid")
        chain.append(eid if eid is not None else f"{u}->{v}")
        chain.append(v)
    return chain



def eval_global_conn_k(
    comps_state: Dict[str, int],
    G_base: nx.Graph
) -> Tuple[int, str, None]:
    """
    Build subgraph H from G_base according to component states:
      - If comps_state[node_id] == 0: remove all edges incident to that node.
      - Only include edges whose comps_state[eid] == 1.
      - Nodes remain present; connectivity is determined by remaining edges.

    Returns:
        (k_value, k_value, None)
    """
    # Collect node-off set and the set of edge IDs marked on/off
    node_off = {cid for cid, st in comps_state.items() if st == 0 and cid in G_base.nodes}
    edge_on  = {cid for cid, st in comps_state.items() if st == 1}  # keep only these edges
    # (unknown IDs in comps_state are ignored)

    # Build subgraph
    H = nx.Graph()
    H.add_nodes_from(G_base.nodes(data=True))

    for u, v, data in G_base.edges(data=True):
        eid = data.get("eid")
        # skip if incident to a node that's off
        if u in node_off or v in node_off:
            continue
        # include only edges explicitly set to 1
        if eid is not None and eid in edge_on:
            H.add_edge(u, v, **data)

    # Compute global vertex connectivity
    k_val = nx.node_connectivity(H) if H.number_of_nodes() > 1 else 0
    return k_val, k_val, None

from typing import Dict, Tuple, Any, Iterable, Optional, List
import networkx as nx

def _pairwise(seq: List[str]):
    for i in range(len(seq) - 1):
        yield seq[i], seq[i + 1]

def _edge_ids_on_path(G: nx.Graph, node_path: Optional[List[str]]) -> Optional[List[Optional[Any]]]:
    """Return [eid1, eid2, ...] along the node_path; None if no path or eid missing."""
    if not node_path:
        return None
    is_multi = isinstance(G, (nx.MultiGraph, nx.MultiDiGraph))
    eids: List[Optional[Any]] = []
    for u, v in _pairwise(node_path):
        eid = None
        if is_multi:
            data_dict = G.get_edge_data(u, v)  # {key: attrdict}
            if data_dict:
                _, d = next(iter(data_dict.items()))
                eid = d.get("eid")
        else:
            d = G.get_edge_data(u, v)
            if d:
                eid = d.get("eid")
        eids.append(eid)
    return eids

def _node_edge_chain(G: nx.Graph, node_path: Optional[List[str]]) -> Optional[List[Any]]:
    """['n1','n3','n6'] -> ['n1', eid(n1,n3), 'n3', eid(n3,n6), 'n6'] (uses 'eid', falls back to 'u->v')."""
    if not node_path:
        return None
    chain: List[Any] = [node_path[0]]
    is_multi = isinstance(G, (nx.MultiGraph, nx.MultiDiGraph))
    for u, v in _pairwise(node_path):
        eid = None
        if is_multi:
            data_dict = G.get_edge_data(u, v)
            if data_dict:
                _, d = next(iter(data_dict.items()))
                eid = d.get("eid")
        else:
            d = G.get_edge_data(u, v)
            if d:
                eid = d.get("eid")
        chain.append(eid if eid is not None else f"{u}->{v}")
        chain.append(v)
    return chain

def eval_travel_time_to_nearest(
    comps_state: Dict[str, int],
    G_base: nx.Graph,
    origin: str,
    destinations: Iterable[str],
    *,
    avg_speed: float = 60.0,        # distance units per hour (e.g., km/h)
    target_max: float = 0.5,        # allowed extra time over baseline, in HOURS
    length_attr: str = "length",    # edge length attribute (e.g., km)
) -> Tuple[Optional[float], str, Dict[str, Any]]:
    dest_set = set(destinations)
    if not dest_set:
        return None, 0, {"reason": "no destinations provided"}

    # ----- Baseline graph (all edges that have length_attr) -----
    Hb = G_base.__class__()
    Hb.add_nodes_from(G_base.nodes(data=True))
    for u, v, data in G_base.edges(data=True):
        if length_attr in data and data[length_attr] is not None:
            Hb.add_edge(u, v, **data)

    if not Hb.has_node(origin):
        return None, 0, {"reason": "origin_missing_in_baseline"}

    cand_b = [d for d in dest_set if Hb.has_node(d)]
    if not cand_b:
        return None, 0, {"reason": "no_destinations_in_baseline"}

    try:
        dist_b_map, paths_b = nx.single_source_dijkstra(Hb, source=origin, weight=length_attr)
    except nx.NetworkXNoPath:
        return None, 0, {"reason": "no_baseline_path"}

    reach_b = [(d, dist_b_map[d]) for d in cand_b if d in dist_b_map]
    if not reach_b:
        return None, 0, {"reason": "no_baseline_destination_reachable"}

    dest_b, dist_b = min(reach_b, key=lambda x: x[1])
    time_b = dist_b / float(avg_speed)  # hours
    path_b_nodes = paths_b.get(dest_b)
    path_b_chain = _node_edge_chain(Hb, path_b_nodes)
    path_b_edges = _edge_ids_on_path(Hb, path_b_nodes)

    # ----- Filtered graph (apply comps_state) -----
    node_off = {cid for cid, st in comps_state.items() if st == 0 and cid in G_base.nodes}
    edge_on  = {cid for cid, st in comps_state.items() if st == 1}

    if origin in node_off:
        return None, 0, {
            "reason": "origin_off",
            "baseline_time_hours": time_b,
            "baseline_path_nodes": path_b_nodes,
            "baseline_path_edges": path_b_edges,
            "baseline_path_chain": path_b_chain,
        }

    H = G_base.__class__()
    H.add_nodes_from(G_base.nodes(data=True))
    for u, v, data in G_base.edges(data=True):
        if u in node_off or v in node_off:
            continue
        eid = data.get("eid")
        if eid is not None and eid in edge_on:
            if length_attr in data and data[length_attr] is not None:
                H.add_edge(u, v, **data)

    if not H.has_node(origin):
        return None, 0, {
            "reason": "origin_missing_in_filtered",
            "baseline_time_hours": time_b,
            "baseline_path_nodes": path_b_nodes,
            "baseline_path_edges": path_b_edges,
            "baseline_path_chain": path_b_chain,
        }

    cand_f = [d for d in dest_set if H.has_node(d) and d not in node_off]
    if not cand_f:
        return None, 0, {
            "reason": "no_destinations_in_filtered",
            "baseline_time_hours": time_b,
            "baseline_path_nodes": path_b_nodes,
            "baseline_path_edges": path_b_edges,
            "baseline_path_chain": path_b_chain,
        }

    try:
        dist_f_map, paths_f = nx.single_source_dijkstra(H, source=origin, weight=length_attr)
    except nx.NetworkXNoPath:
        return None, 0, {
            "reason": "no_path_filtered",
            "baseline_time_hours": time_b,
            "baseline_path_nodes": path_b_nodes,
            "baseline_path_edges": path_b_edges,
            "baseline_path_chain": path_b_chain,
        }

    reach_f = [(d, dist_f_map[d]) for d in cand_f if d in dist_f_map]
    if not reach_f:
        return None, 0, {
            "reason": "no_destination_reachable_filtered",
            "baseline_time_hours": time_b,
            "baseline_path_nodes": path_b_nodes,
            "baseline_path_edges": path_b_edges,
            "baseline_path_chain": path_b_chain,
        }

    dest_f, dist_f = min(reach_f, key=lambda x: x[1])
    time_f = dist_f / float(avg_speed)  # hours
    path_f_nodes = paths_f.get(dest_f)
    path_f_chain = _node_edge_chain(H, path_f_nodes)
    path_f_edges = _edge_ids_on_path(H, path_f_nodes)

    # ----- Threshold check -----
    if isinstance(target_max, (int, float)):
        target_max = [target_max]
    time_threshold = [time_b + float(tm) for tm in target_max]

    sys_st = next((i for i, t in enumerate(time_threshold) if t < time_f), len(time_threshold))

    info = {
        # filtered
        "dest_reached": dest_f,
        "dist_filtered": dist_f,
        "time_filtered_hours": time_f,
        "path_filtered_nodes": path_f_nodes,
        "path_filtered_edges": path_f_edges,  
        "path_filtered_chain": path_f_chain,
        # baseline
        "baseline_dest": dest_b,
        "baseline_dist": dist_b,
        "baseline_time_hours": time_b,
        "baseline_path_nodes": path_b_nodes,
        "baseline_path_edges": path_b_edges,   
        "baseline_path_chain": path_b_chain,
        # params
        "avg_speed_per_hour": avg_speed,
        "allowed_extra_time_hours": target_max,
        "time_threshold_hours": time_threshold,
        "reached_any": True,
    }
    return time_f, sys_st, info