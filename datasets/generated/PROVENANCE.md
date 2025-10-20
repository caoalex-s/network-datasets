# Provenance

This file records the generator settings used for each example dataset.
Commands are shown in Windows **cmd** syntax (line breaks with `^`).

---

## grid_8x8 (v1)
- **Generator**: Grid
- **Parameters**: `rows=8`, `cols=8`, `p_fail=0.1`
- **Command**:
```
python -m ndtools.network_generator ^
  --type grid ^
  --name grid_8x8 ^
  --rows 8 ^
  --cols 8 ^
  --p_fail 0.1 ^
  --description "8x8 grid demo"
```

## er_60_p005 (v1)
- **Generator**: Erdős–Rényi
- **Parameters**: `n_nodes=60`, `p=0.05`, `p_fail=0.05`, `seed=7`
- **Command**:
```
python -m ndtools.network_generator ^
  --type erdos_renyi ^
  --name er_60_p005 ^
  --n_nodes 60 ^
  --p 0.05 ^
  --p_fail 0.05 ^
  --description "ER(60,0.05) demo" --seed 7
```

## ws_n60_k6_b015 (v1)
- **Generator**: Watts–Strogatz
- **Parameters**: `n_nodes=60`, `k=6`, `p_ws=0.15`, `p_fail=0.1`, `seed=7`
- **Command**:
```
python -m ndtools.network_generator ^
  --type ws ^
  --name ws_n60_k6_b015 ^
  --n_nodes 60 ^
  --k 6 ^
  --p_ws 0.15 ^
  --p_fail 0.1 ^
  --seed 7 ^
  --description "Watts–Strogatz graph, n=60, k=6, beta=0.15"
```

## ba_n60_m3 (v1)
- **Generator**: Barabási–Albert
- **Parameters**: `n_nodes=60`, `m=3`, `p_fail=0.1`, `seed=7`
- **Command**:
```
python -m ndtools.network_generator ^
  --type ba ^
  --name ba_n60_m3 ^
  --n_nodes 60 ^
  --m 3 ^
  --p_fail 0.1 ^
  --seed 7 ^
  --description "Barabasi-Albert, n=60, m=3 (~174 edges)"
```

## rg_n60_r017 (v1)
- **Generator**: Random Geometric
- **Parameters**: `n_nodes=60`, `radius=0.17`, `p_fail=0.1`, `seed=7`
- **Command**:
```
python -m ndtools.network_generator ^
  --type rg ^
  --name rg_n60_r017 ^
  --n_nodes 60 ^
  --radius 0.17 ^
  --p_fail 0.1 ^
  --seed 7 ^
  --description "Random geometric graph, n=60, r=0.17 (~150 edges)"
```

## config_n60_deg3 (v1)
- **Generator**: Configuration (avg degree target)
- **Parameters**: `n_nodes=60`, `avg_deg=3.0`, `p_fail=0.1`, `seed=7`
- **Command**:
```
python -m ndtools.network_generator ^
  --type config ^
  --name config_n60_deg3 ^
  --n_nodes 60 ^
  --avg_deg 3 ^
  --p_fail 0.1 ^
  --seed 7 ^
  --description "Configuration model, n=60, avg_deg=3"
```

---

**Notes**
- Edge probabilities in `probs.json` follow the binary schema: `"0": {"p": p_fail}`, `"1": {"p": 1-p_fail}`.
- Layout images are created (if enabled) using `ndtools.graphs.draw_graph_from_data`.
