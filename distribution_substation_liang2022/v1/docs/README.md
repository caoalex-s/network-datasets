# Dataset: dist-sub-110-220kV-liang2022 (v1.0.0)

## Summary
This dataset represents a simplified **110/220 kV distribution substation**
based on Liang (2022). It is intended for demonstration and validation of
network reliability and resilience methods using the **Matrix-based Bayesian Network (MBN)** framework.

## Structure

- `data/nodes.json`  
  Dictionary of nodes with coordinates, type, group name, and capacities.  
  Example entry:
  ```json
  "N1": { "x": 0, "y": 1, "type": "source", "group_name": "G1", "capacity": 100, "unit": "MW" }
  ```
- `data/edges.json`  
  Dictionary of edges with from, to, and macrocomponent_type.  
  Example entry:
  ```json
  "E1": { "from": "N1", "to": "N2", "directed": true, "macrocomponent_type": "M_BC110_1" }
  ```
- `data/probs.json`  
  Dictionary of edge failure probabilities.  
  Example entry:
  ```json
  "E1": { "0": { "p": 0.05 },"1": { "p": 0.95 } }
  ```

- `data/equipment.json`  
  Fragility parameters (mu, beta) for each equipment type.

- `data/macrocomponents.json`  
  Maps macrocomponent types to equipment counts.

- `scripts/utils.py`  
  Helper functions for data processing and system analysis following Liang (2022)'s framework.

- `scripts/demo_sys_fun.ipynb`
  Demonstration script to analyse network performance (maximum processible capacity) using the helper functions.

  - `scripts/demo_edge_prob_update.ipynb` 
  Demonstration script to update edge failure probabilities, provided a design PGA value.

## Data Dictionary

### Nodes
- x, y — schematic coordinates (not geodetic).
- type — {source, input, transmission, output}.
- group_name — functional grouping (e.g. I1, I2).
- capacity — available capacity.
- unit — units of capacity.

### Edges
- from, to — node IDs.
- macrocomponent_type — identifier linking to macrocomponents.json.

### Macrocomponents
- equipment_number: number of equipment items per type

### Equipment
- mu, beta — lognormal fragility parameters.


## Usage

  ```python
  from pathlib import Path
  import json

  root = Path("distribution-substation-liang2022/v1")

  with open(root / "data" / "nodes.json", "r") as f:
      nodes = json.load(f)

  with open(root / "data" / "edges.json", "r") as f:
      edges = json.load(f)

  with open(root / "data" / "probs.json", "r") as f:
      probs = json.load(f)
  ```