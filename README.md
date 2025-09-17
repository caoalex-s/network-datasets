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
├─ ndtools/ # Utility functions for loading, graph building, and general network functions
├─ tests/ # Unit tests
└─ LICENSE # Licensing (MIT for code, CC-BY-4.0 for data)
```

---

## Installation

You can install the tools `ndtools` into your Python environment.

### Using pip (editable install)
From the repository root:

```bash
# First activate your conda environment (if using conda)
conda activate <your-env>

# Then install in editable mode
pip install -e .
```

This makes the `ndtools` package importable anywhere in that environment.

### Verify installation
```bash
python -c "import ndtools; print(ndtools.__version__)"
```

### Run tests
```bash
pytest -q
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
