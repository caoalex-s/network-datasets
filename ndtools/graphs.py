import networkx as nx
from typing import Dict, Any, Optional

import json
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path

def build_graph(
    nodes: Dict[str, Dict[str, Any]],
    edges: Dict[str, Dict[str, Any]],
    probs: Optional[Dict[str, Any]] = None,
) -> nx.Graph:
    G = nx.Graph()
    for nid, attrs in nodes.items():
        G.add_node(nid, **attrs)
    for eid, e in edges.items():
        u, v = e["from"], e["to"]
        attr = {"eid": eid, **{k: v for k, v in e.items() if k not in ("from","to")}}
        if probs is not None:
            attr["p_active"] = probs.get(eid, {}).get("1", {}).get("p", None)
        G.add_edge(u, v, **attr)
    return G

def draw_graph_from_data(
    data_dir: str | Path,
    *,
    layout: str = "spring",
    node_color: str = "skyblue",
    node_size: int = 500,
    edge_color: str = "gray",
    with_node_labels: bool = True,
    with_edge_labels: bool = False,
    title: Optional[str] = None,
    layout_kwargs: Optional[Dict[str, Any]] = None,
    output_name: str = "graph.png",
) -> Path:
    """
    Load nodes/edges from JSON files in `data_dir`, draw the graph, and save to the same dir.

    Expects:
        - nodes.json : [{"id": "A", "attr1": ..., ...}, ...]
        - edges.json : [{"source": "A", "target": "B", "eid": "e1", "attr2": ..., ...}, ...]

    Args:
        data_dir: Directory containing nodes.json and edges.json.
        layout: Layout algorithm ("spring", "kamada_kawai", "circular", "shell").
        node_color: Color for nodes.
        node_size: Node size in points^2.
        edge_color: Color for edges.
        with_node_labels: Whether to display node labels.
        with_edge_labels: Whether to display edge labels (uses 'eid' if present).
        title: Optional title for the plot.
        layout_kwargs: Optional kwargs passed to the layout function.
        output_name: Filename of the saved image (saved under data_dir).

    Returns:
        Path to the saved image file.

    Example usage:
        draw_graph_from_data("ema_highway/v1/data")
    """
    def _extract_positions(G, x_key="x", y_key="y"):
        """Return {node: (x,y)} using x/y or pos_x/pos_y if present."""
        pos = {}
        for n, d in G.nodes(data=True):
            if x_key in d and y_key in d:
                pos[n] = (float(d[x_key]), float(d[y_key]))
            elif "pos_x" in d and "pos_y" in d:
                pos[n] = (float(d["pos_x"]), float(d["pos_y"]))
        return pos

    data_dir = Path(data_dir)
    layout_kwargs = layout_kwargs or {}

    # --- Load nodes & edges ---
    nodes_path = data_dir / "nodes.json"
    edges_path = data_dir / "edges.json"

    with open(nodes_path, "r", encoding="utf-8") as f:
        nodes = json.load(f)

    with open(edges_path, "r", encoding="utf-8") as f:
        edges = json.load(f)

    # --- Build graph ---
    # Peek at the first edge
    first_key, first_val = next(iter(edges.items()))
    is_directed = bool(first_val.get("directed", False))
    # Choose graph type
    G = nx.DiGraph() if is_directed else nx.Graph()

    for nid, nv in nodes.items():
        attrs = {k: v for k, v in nv.items()}
        G.add_node(nid, **attrs)

    for e, ev in edges.items():
        u, v = ev["from"], ev["to"]
        attrs = {k: v for k, v in ev.items() if k not in ("from", "to", "directed")}
        G.add_edge(u, v, **attrs)

    # --- Pick layout ---
    if layout == "spring":
        pos = nx.spring_layout(G, **layout_kwargs)
    elif layout == "kamada_kawai":
        pos = nx.kamada_kawai_layout(G, **layout_kwargs)
    elif layout == "circular":
        pos = nx.circular_layout(G, **layout_kwargs)
    elif layout == "shell":
        pos = nx.shell_layout(G, **layout_kwargs)
    else:
        raise ValueError(f"Unknown layout: {layout}")

    # --- Draw ---
    # Try to use embedded positions first
    pos = _extract_positions(G)

    # If no embedded positions, fall back to a layout algorithm
    if not pos:
        if layout == "spring":
            pos = nx.spring_layout(G, **layout_kwargs)
        elif layout == "kamada_kawai":
            pos = nx.kamada_kawai_layout(G, **layout_kwargs)
        elif layout == "circular":
            pos = nx.circular_layout(G, **layout_kwargs)
        elif layout == "shell":
            pos = nx.shell_layout(G, **layout_kwargs)
        else:
            raise ValueError(f"Unknown layout: {layout}")
    
    plt.figure(figsize=(8, 6))
    nx.draw(
        G,
        pos,
        node_color=node_color,
        node_size=node_size,
        edge_color=edge_color,
        with_labels=with_node_labels,
        font_size=9,
        font_color="black",
    )

    if with_edge_labels:
        edge_labels = {
            (u, v): d.get("eid", "")
            for u, v, d in G.edges(data=True)
        }
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    if title:
        plt.title(title)

    # --- Save ---
    out_path = data_dir / output_name
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()

    return out_path

