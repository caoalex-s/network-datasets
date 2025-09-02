# Network Datasets

A curated collection of example infrastructure network datasets for reliability and resilience research.

This repository provides structured datasets (nodes, edges, probabilities, and optional metadata) along with JSON Schemas for validation.  
The datasets are designed for use with [MBNpy](https://github.com/jieunbyun/mbnpy) but can also be loaded directly with Python.

---

## Repository structure
```
├─ registry.json # Index of available datasets
├─ schema/ # JSON Schemas for validation
├─ <dataset folders>/ # e.g. distribution-substation-liang2022/, ...
└─ LICENSE # Licensing (MIT for code, CC-BY-4.0 for data)
```

---

## Usage

### Example load directly in Python
```python
import json
from pathlib import Path

# Example dataset
root = Path("distribution-substation-liang2022/v1") 

nodes = json.loads((root/"data/nodes.json").read_text())
edges = json.loads((root/"data/edges.json").read_text())
probs = json.loads((root/"data/probs.json").read_text())
```

### Validate against schemas
```python
pip install jsonschema
python data_validate.py --root . # Check all repos
python data_validate.py --root . --dataset distribution-substation-liang2022 # Check specific dataset
```

## License
- Code (scripts, validators): MIT License
- Data (datasets): CC-BY-4.0 License
