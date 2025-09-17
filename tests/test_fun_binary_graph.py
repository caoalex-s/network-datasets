import json
from pathlib import Path
from typing import Dict, Any, Tuple

import networkx as nx
import pytest

# Import the function under test
from ndtools import fun_binary_graph

# ---------- helpers ----------

def load_dataset(dataset_dir: Path) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    with open(dataset_dir / "nodes.json", "r", encoding="utf-8") as f:
        nodes = json.load(f)
    with open(dataset_dir / "edges.json", "r", encoding="utf-8") as f:
        edges = json.load(f)
    with open(dataset_dir / "probs.json", "r", encoding="utf-8") as f:
        probs = json.load(f)  # not strictly needed here, but handy later
    return nodes, edges, probs

def build_base_graph(nodes: Dict[str, Dict[str, Any]],
                     edges: Dict[str, Dict[str, Any]]) -> nx.Graph:
    """Build an undirected base graph with 'eid' stored on each edge."""
    G = nx.Graph()
    for nid, attrs in nodes.items():
        G.add_node(nid, **attrs)
    for eid, e in edges.items():
        u, v = e["from"], e["to"]
        # keep any extra attributes except endpoints
        attr = {"eid": eid, **{k: v for k, v in e.items() if k not in ("from", "to")}}
        G.add_edge(u, v, **attr)
    return G

def dataset_path() -> Path:
    """
    Resolve the dataset dir relative to the repo root:
    <repo_root>/toynet-11edges/v1/data
    """
    here = Path(__file__).resolve()
    repo_root = here.parents[1]  # go up to repo root (…/tests/..)
    return repo_root / "toynet-11edges" / "v1" / "data"

def dataset_path_ema() -> Path:
    """
    Resolve the EMA dataset dir relative to the repo root:
    <repo_root>/ema_highway/v1/data
    """
    here = Path(__file__).resolve()
    repo_root = here.parents[1]  # .../tests/..
    return repo_root / "ema_highway" / "v1" / "data"

# ---------- fixtures ----------

@pytest.fixture(scope="session")
def toy_data():
    nodes, edges, probs = load_dataset(dataset_path())
    return nodes, edges, probs

@pytest.fixture(scope="session")
def G_base(toy_data):
    nodes, edges, _ = toy_data
    return build_base_graph(nodes, edges)

# ---------- tests ----------

def test_eval_global_conn_k1(G_base: nx.Graph, toy_data):
    nodes, edges, _ = toy_data

    comps_st = {eid: 1 for eid in edges}  # all components survive
    k_val, sys_st, _ = fun_binary_graph.eval_global_conn_k(comps_st, G_base, target_k= 1)

    assert sys_st == 's', f"Expected system state 's', got '{sys_st}'"
    assert k_val == 2, f"Expected k_val 2, got {k_val}"

def test_eval_global_conn_k2(G_base: nx.Graph, toy_data):
    nodes, edges, _ = toy_data

    comps_st = {eid: 1 for eid in edges}  
    comps_st['e01'], comps_st['e02'] = 0, 0  # fail two edges
    k_val, sys_st, _ = fun_binary_graph.eval_global_conn_k(comps_st, G_base, target_k= 1)

    assert sys_st == 's', f"Expected system state 's', got '{sys_st}'"
    assert k_val == 1, f"Expected k_val 1, got {k_val}"

def test_eval_global_conn_k3(G_base: nx.Graph, toy_data):
    nodes, edges, _ = toy_data

    comps_st = {eid: 1 for eid in edges}  
    comps_st['e01'], comps_st['e02'], comps_st['e03'] = 0, 0, 0  # fail three edges
    k_val, sys_st, _ = fun_binary_graph.eval_global_conn_k(comps_st, G_base, target_k= 1)

    assert sys_st == 'f', f"Expected system state 'f', got '{sys_st}'"
    assert k_val == 0, f"Expected k_val 0, got {k_val}"

def test_eval_global_conn_k4(G_base: nx.Graph, toy_data):
    nodes, edges, _ = toy_data

    comps_st = {eid: 1 for eid in edges}  
    comps_st['e05'], comps_st['e06'] = 0, 0  # fail two edges
    k_val, sys_st, _ = fun_binary_graph.eval_global_conn_k(comps_st, G_base, target_k= 2)

    assert sys_st == 'f', f"Expected system state 'f', got '{sys_st}'"
    assert k_val == 1, f"Expected k_val 1, got {k_val}"

def test_eval_travel_time_to_nearest1():
