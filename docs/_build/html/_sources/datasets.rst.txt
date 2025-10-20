Available Datasets
===================

This page provides detailed information about the datasets available in the Network Datasets repository.

Dataset Registry
----------------

All available datasets are listed in the ``registry.json`` file. Each dataset entry includes:

* **name**: Unique identifier for the dataset
* **version**: Dataset version number
* **path**: Relative path to the dataset files
* **summary**: Brief description of the dataset
* **license**: License information (typically CC-BY-4.0)

Current Datasets
----------------

toynet-11edges
~~~~~~~~~~~~~~

* **Version**: 1.0.0  
* **License**: CC-BY-4.0  
* **Path**: ``datasets/toynet-11edges/v1``

A small toy network with 8 nodes and 11 edges, designed for testing and learning purposes.

**Files**:

* ``nodes.json``: Node definitions with coordinates
* ``edges.json``: Edge definitions connecting nodes
* ``probs.json``: Edge failure probabilities

**Use Cases**:

* Testing algorithms and functions
* Learning the data format
* Quick prototyping

ema-highway
~~~~~~~~~~~

* **Version**: 1.0.0  
* **License**: CC-BY-4.0  
* **Path**: ``datasets/ema-highway/v1``

Eastern Massachusetts benchmark highway network with nodes, edges, and probability files.

**Files**:

* ``nodes.json``: Highway intersection nodes
* ``edges.json``: Road segments between intersections
* ``probs_bin.json``: Binary failure probabilities
* ``probs_mult.json``: Multi-state failure probabilities

**Example reference**:
   Byun, J.-E., Ryu, H., & Straub, D. (2025). Branch-and-bound algorithm for efficient reliability analysis of general coherent systems. Structural Safety, 102653.

**Use Cases**:

* Transportation network analysis
* Connectivity to critical facilities 
* Connectivity between communities
* Emergency response planning

Generated Example Collection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``datasets/generated/`` directory contains **synthetic example datasets** produced with
``ndtools.network_generator``. These examples are intended for tutorials, quick tests,
and format demonstrations. They follow the same JSON schemas as all curated datasets.

.. note::
   See :file:`datasets/generated/README.md` for an overview, and :file:`datasets/generated/PROVENANCE.md`
   for the exact commands and parameters used to generate each example.

**Layout**

Each example resides in its own subdirectory with versioning:

.. code-block:: text

   generated/
     grid_8x8/
       v1/data/{nodes.json, edges.json, probs.json, graph.png}
     er_60_p005/
       v1/data/{...}
     ws_n60_k6_b015/
       v1/data/{...}
     ba_n60_m3/
       v1/data/{...}
     rg_n60_r017/
       v1/data/{...}
     config_n60_deg3/
       v1/data/{...}
     README.md
     PROVENANCE.md
     CHANGELOG.md

**What’s inside each example**

- :file:`nodes.json` — map of node id → attributes (at minimum: ``x``, ``y``)
- :file:`edges.json` — map of edge id → ``{from, to, directed, ...}``
- :file:`probs.json` — per-edge binary probabilities (e.g., ``"0"``=failure, ``"1"``=working)
- :file:`graph.png` — (optional) auto-rendered preview

**Reproducibility & provenance**

Each example’s parameters (model family, size, probabilities, seed, etc.) are recorded in
:file:`generated/metadata.json` inside the dataset folder and summarized across the collection in
:file:`generated/PROVENANCE.md`. Regenerate or extend the collection via the CLI examples shown there.

distribution-substation-liang2022
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Version**: 1.0.0  
* **License**: CC-BY-4.0  
* **Path**: ``datasets/distribution-substation-liang2022/v1``

Example 110/220 kV distribution substation network based on Liang et al. (2022). Includes nodes, edges, macrocomponents, equipment fragility, and probability files.

**Files**:

* ``nodes.json``: Substation nodes with coordinates and attributes
* ``edges.json``: Power line connections between substations
* ``probs.json``: Edge failure probabilities
* ``macrocomponents.json``: Component grouping information
* ``equipment.json``: Equipment fragility data

**Citation**:
   Liang, H., Blagojevic, N., Xie, Q., & Stojadinovic, B. (2022). Seismic risk analysis of electrical substations based on the network analysis method. Earthquake Engineering & Structural Dynamics, 51(11), 2690-2707.

**Use Cases**:

* Power grid reliability analysis
* Seismic risk assessment
* Infrastructure resilience studies

Data Format
-----------

All datasets follow a consistent JSON format defined by JSON schemas in the ``schema/`` directory.

Node Format
~~~~~~~~~~~

Nodes are stored as a JSON object where keys are node IDs and values are attribute dictionaries:

.. code-block:: json

   {
     "node_id": {
       "x": 0.0,
       "y": 0.0,
       "type": "source",
       "additional_attributes": "..."
     }
   }

**Required attributes**:

* ``x``: X-coordinate (number)
* ``y``: Y-coordinate (number)

**Examples of optional attributes**:

* ``type``: Node type (string)
* ``group_name``: Grouping identifier (string)
* ``capacity``: Capacity value (number or string)
* ``unit``: Unit of measurement (string)
* Any other custom attributes

Edge Format
~~~~~~~~~~~

Edges are stored as a JSON object where keys are edge IDs and values are connection dictionaries:

.. code-block:: json

   {
     "edge_id": {
       "from": "node1",
       "to": "node2",
       "directed": false,
       "additional_attributes": "..."
     }
   }

**Required attributes**:

* ``from``: Source node ID (string)
* ``to``: Target node ID (string)
* ``directed``: Whether edge is directed (boolean)

**Examples of optional attributes**:

* ``eid``: Edge identifier (string)
* ``macrocomponent_type``: Component type (string)
* ``length``: Edge length (number)
* Any other custom attributes

Probability Format
~~~~~~~~~~~~~~~~~~

Probabilities are stored as a JSON object mapping edge IDs to probability dictionaries:

.. code-block:: json

   {
     "edge_id": {
       "0": {"p": 0.05},
       "1": {"p": 0.95}
     }
   }

Where, for example, ``"1"` indicates the edge could imply active/working and ``"0"` failure.

**Required attributes**:

* ``int``: Integer state index starting from 0
* ``p``: Probability of the state (number between 0 and 1)

**Examples of optional attributes**:

* ``description``: Description of the state (string)

Dataset Metadata
----------------

Each dataset includes a ``dataset.yaml`` file with metadata:

.. code-block:: yaml

   name: dataset-name
   version: 1.0.0
   title: Human-readable title
   license: CC-BY-4.0
   description: >
     Detailed description of the dataset
   contacts:
     - name: Contact Name
       affiliation: Institution
       email: contact@example.com
   tags: [tag1, tag2, tag3]
   files:
     nodes: data/nodes.json
     edges: data/edges.json
     probs: data/probs.json
   citation: |
     Citation information

Loading Datasets
----------------

Using ndtools
~~~~~~~~~~~~~

.. code-block:: python

   from ndtools.io import dataset_paths, load_json
   from pathlib import Path

   # Get dataset paths
   nodes_path, edges_path, probs_path = dataset_paths(
       Path('datasets'), 'dataset_name', 'v1'
   )
   
   # Load data
   nodes = load_json(nodes_path)
   edges = load_json(edges_path)
   probs = load_json(probs_path)

Direct Loading
~~~~~~~~~~~~~~

.. code-block:: python

   import json
   from pathlib import Path

   dataset_path = Path("datasets/dataset_name/v1/data")
   
   with open(dataset_path / "nodes.json") as f:
       nodes = json.load(f)
   
   with open(dataset_path / "edges.json") as f:
       edges = json.load(f)
   
   with open(dataset_path / "probs.json") as f:
       probs = json.load(f)

Validation
----------

All datasets can be validated against their schemas:

.. code-block:: bash

   # Validate all datasets
   python data_validate.py --root .

   # Validate specific dataset
   python data_validate.py --root . --dataset dataset-name

Adding New Datasets
-------------------

To add a new dataset to the repository:

1. Create a new directory following the naming convention: ``dataset_name/v1/`` (⚠️ **Don’t use hyphens (`-`)** — use **underscores (`_`)** in dataset names.)
2. Add your data files in the ``data/`` subdirectory
3. Create a ``dataset.yaml`` metadata file
4. Update the ``registry.json`` file
5. Validate your dataset using the provided validation tools

See the :doc:`contributing` page for detailed instructions.
