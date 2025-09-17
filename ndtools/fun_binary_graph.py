from typing import Dict, Tuple, Any, Iterable, Optional
import networkx as nx


def eval_global_conn_k(
    comps_state: Dict[str, int],
    G_base: nx.Graph,
    target_k: int,
) -> Tuple[int, str, None]:
    """
    Build subgraph H from G_base according to component states:
      - If comps_state[node_id] == 0: remove all edges incident to that node.
      - Only include edges whose comps_state[eid] == 1.
      - Nodes remain present; connectivity is determined by remaining edges.

    Returns:
        (k_value, 's' if k_value >= target_k else 'f', None)
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
    status = 's' if k_val >= target_k else 'f'
    return k_val, status, None

def eval_travel_time_to_nearest(
    comps_state: Dict[str, int],
    G_base: nx.Graph,
    origin: str,
    destinations: Iterable[str],
    *,
    avg_speed_kmh: float = 60.0,
    target_max_minutes: float = 30.0,
    length_attr: str = "length_km",
) -> Tuple[Optional[float], str, Dict[str, Any]]:
    """
    Evaluate the shortest-path travel time (in minutes) from `origin` to the
    nearest node in `destinations`, after applying component states.

    Component-state handling (mirrors your previous function):
      - If comps_state[node_id] == 0: treat that node as OFF -> remove all incident edges.
      - Only include edges whose comps_state[eid] == 1 (edges without eid==1 are excluded).
      - Nodes remain present in H, but connectivity is defined by remaining edges.

    Edge weights:
      - Uses edge attribute `length_attr` (default 'length_km') as distance.
      - Travel time (minutes) = distance_km / avg_speed_kmh * 60.

    Returns:
        (time_minutes, status, info)
        - time_minutes: shortest travel time in minutes to the closest destination,
                        or None if no feasible path exists.
        - status: 's' if time_minutes <= target_max_minutes, else 'f'.
                  If no path exists, status is 'f'.
        - info: dict with details (dest_reached, dist_km, path, reached_any, reason, etc.)
    """
    dest_set = set(destinations)
    if not dest_set:
        return None, 'f', {"reason": "no destinations provided"}

    # Identify nodes switched off and edges switched on
    node_off = {cid for cid, st in comps_state.items() if st == 0 and cid in G_base.nodes}
    edge_on  = {cid for cid, st in comps_state.items() if st == 1}

    # Quick rejection if origin is off or all destinations are off
    if origin in node_off:
        return None, 'f', {"reason": "origin_off"}

    if dest_set.issubset(node_off):
        return None, 'f', {"reason": "all_destinations_off"}

    # Build filtered subgraph H
    H = nx.Graph()
    H.add_nodes_from(G_base.nodes(data=True))

    for u, v, data in G_base.edges(data=True):
        eid = data.get("eid")
        # skip edges incident to OFF nodes
        if u in node_off or v in node_off:
            continue
        # include only edges explicitly set to 1
        if eid is not None and eid in edge_on:
            # require a valid distance attribute
            if length_attr in data and data[length_attr] is not None:
                H.add_edge(u, v, **data)

    # If origin or all dests are isolated/missing after filtering, fail fast
    if not H.has_node(origin):
        return None, 'f', {"reason": "origin_missing_in_H"}

    # Keep only destinations that remain in H and are not off
    candidate_dests = [d for d in dest_set if H.has_node(d) and d not in node_off]
    if not candidate_dests:
        return None, 'f', {"reason": "no_destinations_in_H"}

    # Compute shortest paths from origin using the given length attribute
    try:
        # Single-source Dijkstra distances (and paths) is efficient for many destinations
        dist, paths = nx.single_source_dijkstra(H, source=origin, weight=length_attr)
    except nx.NetworkXNoPath:
        return None, 'f', {"reason": "no_path"}

    # Find nearest destination among those reachable
    reachable = [(d, dist[d]) for d in candidate_dests if d in dist]
    if not reachable:
        return None, 'f', {"reason": "no_destination_reachable"}

    dest_reached, dist_km = min(reachable, key=lambda x: x[1])

    # Convert distance to time (minutes)
    time_minutes = (dist_km / float(avg_speed_kmh)) * 60.0

    status = 's' if time_minutes <= float(target_max_minutes) else 'f'
    info = {
        "dest_reached": dest_reached,
        "dist_km": dist_km,
        "time_minutes": time_minutes,
        "path": paths.get(dest_reached),
        "avg_speed_kmh": avg_speed_kmh,
        "target_max_minutes": target_max_minutes,
        "reached_any": True,
    }
    return time_minutes, status, info