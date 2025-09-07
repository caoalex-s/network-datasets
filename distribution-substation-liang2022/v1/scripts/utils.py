import networkx as nx
import numpy as np
from scipy.stats import norm
import json

def has_path_from_multiple_sources(G, sources, target_node):
    for s in sources:
        if nx.has_path(G, s, target_node):
            return True
    return False

def has_path_to_multiple_targets(G, source_node, targets):
    for t in targets:
        if nx.has_path(G, source_node, t):
            return True
    return False

def process_nodes(nodes):
    node_groups = {}
    node_groups['source'] = [k for k, v in nodes.items() if v['type'] == 'source']

    node_groups['input'] = {}
    for k, v in nodes.items():
        if v['type'] == 'input':
            if v['group_name'] in node_groups['input']:
                node_groups['input'][v['group_name']].append(k)
            else:
                node_groups['input'][v['group_name']] = [k]

    node_groups['output'] = {}
    node_groups['output_list'] = []
    for k, v in nodes.items():
        if v['type'] == 'output':
            node_groups['output_list'].append(k)
            if v['group_name'] in node_groups['output']:
                node_groups['output'][v['group_name']].append(k)
            else:
                node_groups['output'][v['group_name']] = [k]
    
    node_groups['transmission'] = {}
    for k, v in nodes.items():
        if v['type'] == 'transmission':
            if v['group_name'] in node_groups['transmission']:
                node_groups['transmission'][v['group_name']].append(k)
            else:
                node_groups['transmission'][v['group_name']] = [k]
    
    return node_groups

def sys_fun(comps_st, edges, nodes, node_groups, return_details=False):

    G = nx.DiGraph()
    for k, v in edges.items():
        if comps_st[k] == 1:
            G.add_edge(v["from"], v["to"], name=k)
    for k, v in nodes.items():
        G.add_node(k)

    # Check inputs
    TC_I_list = []
    for k, v in node_groups['input'].items():
        has_path_ = []
        capa_ = nodes[v[0]]['capacity'] # all inputs in the same group have the same capacity
        for n in v:
            has_path_source = has_path_from_multiple_sources(G, node_groups['source'], n)

            has_path_output = has_path_to_multiple_targets(G, n, node_groups['output_list'])

            has_path_.append(has_path_source and has_path_output)
        
        if all(has_path_):
            TC_val = capa_ * 1.2
        elif any(has_path_):
            TC_val = capa_
        else:
            TC_val = 0.0
        
        TC_I_list.append(TC_val)
    EI = sum(TC_I_list)

    # Check outputs
    TC_O_list = []
    for k, v in node_groups['output'].items():
        has_path_ = []
        capa_ = nodes[v[0]]['capacity'] # all outputs in the same group have the same capacity
        for n in v:
            has_path_source = has_path_from_multiple_sources(G, node_groups['source'], n)
            
            has_path_.append(has_path_source)
        
        if all(has_path_):
            TC_val = capa_ * 1.2
        elif any(has_path_):
            TC_val = capa_
        else:
            TC_val = 0.0
        
        TC_O_list.append(TC_val)
    EO = sum(TC_O_list)

    # Check transmission
    TC_T_list = []
    for k, v in node_groups['transmission'].items():
        has_path_ = []
        capa_ = nodes[v[0]]['capacity'] # all transmission in the same group have the same capacity
        for n in v:
            has_path_source = has_path_from_multiple_sources(G, node_groups['source'], n)

            has_path_output = has_path_to_multiple_targets(G, n, node_groups['output_list'])

            has_path_.append(has_path_source and has_path_output)
        
        if any(has_path_):
            TC_val = capa_
        else:
            TC_val = 0.0
        
        TC_T_list.append(TC_val)

    ET = sum(TC_T_list)

    F_ds = min(EI, EO, ET)

    if return_details is False:
        return F_ds
    else:
        return {
            "System capacity": F_ds,
            "Total input": EI,
            "Total output": EO,
            "Total transmission": ET,
            "Input breakdowns": TC_I_list,
            "Output breakdowns": TC_O_list,
            "Transmission breakdowns": TC_T_list
        }

def cal_fail_prob(equip_entry: dict, pga: float) -> float:
    """
    Compute expected failure probability for a given equipment entry and PGA.
    
    Parameters
    ----------
    equip_entry : dict
        Dictionary containing fragility parameters {"mu": ..., "beta": ...}
    pga : float
        Design ground acceleration
    
    Returns
    -------
    float
        Failure probability (0–1)
    """
    mu = equip_entry["fragility"]["mu"]
    beta = equip_entry["fragility"]["beta"]
    
    # lognormal fragility function
    z = (np.log(pga) - np.log(mu)) / beta
    return float(norm.cdf(z))

def get_edge_probs(pga: float) -> dict:
    """
    Compute failure probabilities for edges based on PGA.
    Save the file as ../data/probs.ipynb

    Parameters
    ----------
    pga : float
        Design ground acceleration

    Returns
    -------
    dict
        Dictionary of {edge: {0: <pf>, 1: <1.-pf>}}
    """

    with open("../data/edges.json", "r") as file:
        edges = json.load(file)

    with open('../data/macrocomponents.json', 'r') as file:
        mcomp = json.load(file)

    with open('../data/equipment.json', 'r') as file:
        equip = json.load(file)

    for k, v in equip.items():
        equip[k]['pf'] = cal_fail_prob(v, pga)

    probs = {}
    for e, v in edges.items():
        equip_e = mcomp[v['macrocomponent_type']]
        
        ps = 1.0 # survival probability
        for k, v in equip_e['equipment_number'].items():
            # ps *= (1.0 - equip[k]['pf']) ** v # Too high failure probability
            ps *= (1.0 - equip[k]['pf'])
        probs[e] = {0: {"p":1.0 - ps}, 1: {"p": ps}}

    with open('../data/probs.json', 'w') as file:
        json.dump(probs, file, indent=4)
        print("Saved ../data/probs.json")

    return probs