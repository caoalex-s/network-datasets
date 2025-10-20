# Dataset: ema-highway (v1.0.0)

## Summary
**Eastern Massachusetts (EMA) highway benchmark network** with nodes, edges, and a probability file.
This package is intended for testing network reliability / resilience algorithms (e.g., MBN/BN-based)
and path-based analyses on a mid-sized, schematic road network.

## Structure
- `data/nodes.json`  
  Dictionary of node IDs to schematic coordinates (km). Example:
  ```json
  "n1": { "x": 110.245232, "y": 139.0 }
  ```

- `data/edges.json`  
  Dictionary of undirected links with fields `from`, `to`, and `directed` (here `false`). Example:
  ```json
  "e0001": { "from": "n1", "to": "n2", "directed": false }
  ```

- `data/probs_bin.json`  
  The exact semantics depend on your analysis. Example minimal shape (per edge):
  ```json
  "e0001": {"0": {"p": 0.05}, "1": {"p": 0.95}}
  ```

- `data/probs_mult.json`
  Example minimal shape (per edge):
  ```json
  "e0001": {"0": {"p": 0.05}, "1": {"p": 0.10}, "2": {"p": 0.85}}
  ```

## Data Dictionary
### Nodes (`nodes.json`)
- `x`, `y` — schematic coordinates in kilometers (not geodetic).

### Edges (`edges.json`)
- `from`, `to` — node IDs (strings matching `nodes.json` keys).
- `directed` — boolean (this dataset uses `false`).
- `length_km` — length of edge in km, computed from node coordinates.

### Probabilities (`probs_bin.json` and `probs_mult.json`)
- Keyed by edge ID, with state/probability entries (format may vary by method).

## Usage
```python
from pathlib import Path
import json

root = Path("ema-highway/v1/data")

nodes = json.loads((root / "nodes.json").read_text("utf-8"))
edges = json.loads((root / "edges.json").read_text("utf-8"))
probs = json.loads((root / "probs.json").read_text("utf-8"))  # if used
```

## Notes
- Coordinates in `nodes.json` are planar coordinates in kilometres (not geodetic).
