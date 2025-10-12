# Example Datasets (generated/)

This directory contains **example network datasets** produced by `ndtools.network_generator`.
Each dataset is self-contained and validated against the repository schemas.

```
generated/
  ba_n60_m3/
    v1/data/...
  config_n60_deg3/
    v1/data/...
  er_60_p005/
    v1/data/...
  grid_8x8/
    v1/data/...
  rg_n60_r017/
    v1/data/...
  ws_n60_k6_b015/
    v1/data/...
  README.md
  PROVENANCE.md
  CHANGELOG.md
```

## What is inside a dataset?

For each dataset, files live under: `generated/<name>/v1/data/`

- **nodes.json** — a *map* of node id → attributes  
  Example (grid):  
  ```json
  {
    "n0": {"x": 0, "y": 0},
    "n1": {"x": 1, "y": 0},
    "...": "..."
  }
  ```

- **edges.json** — a *map* of edge id → `{from, to, directed, ...}`  
  Example:  
  ```json
  {
    "e0": {"from": "n0", "to": "n1", "directed": false},
    "e1": {"from": "n0", "to": "n8", "directed": false}
  }
  ```

- **probs.json** — per-edge binary-state probabilities (failure/survival)  
  Example:  
  ```json
  {
    "e0": {"0": {"p": 0.1}, "1": {"p": 0.9}}
  }
  ```

- **graph.png** — (optional) quick preview figure rendered by `ndtools.graphs.draw_graph_from_data`.

## Included example datasets

- `grid_8x8` — 8×8 lattice with integer coordinates.  
- `er_60_p005` — Erdős–Rényi with `n=60`, `p=0.05`.  
- `ws_n60_k6_b015` — Watts–Strogatz with `n=60`, `k=6`, `β=0.15`.  
- `ba_n60_m3` — Barabási–Albert with `n=60`, `m=3`.  
- `rg_n60_r017` — Random Geometric in unit square with `n=60`, `radius=0.17`.  
- `config_n60_deg3` — Configuration model targeting average degree ≈ `3.0` (≈ 90 edges).

> Tip: Regenerate or add new datasets with `python -m ndtools.network_generator ...`

## Viewing the graphs

If `graph.png` is present it shows a quick layout-based preview.  
You can re-render at any time:

```bash
python - <<'PY'
from ndtools.graphs import draw_graph_from_data
from pathlib import Path
draw_graph_from_data(Path('generated/grid_8x8/v1/data'))
PY
```

## Acknowledgments

The network generator extensions were drafted by **`Alex Sixie Cao <https://scholar.google.com/citations?user=QUu8BdEAAAAJ&hl=en>`_**.
\