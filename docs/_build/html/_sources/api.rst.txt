API Reference
=============

This page provides detailed API documentation for all functions and classes in the ndtools package.

IO Module
---------

.. automodule:: ndtools.io
   :members:
   :undoc-members:
   :show-inheritance:

Graphs Module
-------------

.. automodule:: ndtools.graphs
   :members:
   :undoc-members:
   :show-inheritance:

Binary Graph Functions Module
-----------------------------

.. automodule:: ndtools.fun_binary_graph
   :members:
   :undoc-members:
   :show-inheritance:

Function Details
================

Data Loading Functions
----------------------

.. autofunction:: ndtools.io.load_json
   :noindex:

.. autofunction:: ndtools.io.load_yaml
   :noindex:

.. autofunction:: ndtools.io.dataset_paths
   :noindex:

Graph Construction Functions
----------------------------

.. autofunction:: ndtools.graphs.build_graph
   :noindex:

.. autofunction:: ndtools.graphs.compute_edge_lengths
   :noindex:

Visualization Functions
-----------------------

.. autofunction:: ndtools.graphs.draw_graph_from_data
   :noindex:

System Function Evaluation
--------------------------

.. autofunction:: ndtools.fun_binary_graph.eval_global_conn_k
   :noindex:

.. autofunction:: ndtools.fun_binary_graph.eval_travel_time_to_nearest
   :noindex:

Helper Functions
----------------

.. autofunction:: ndtools.fun_binary_graph._pairwise
   :noindex:

.. autofunction:: ndtools.fun_binary_graph._edge_ids_on_path
   :noindex:

.. autofunction:: ndtools.fun_binary_graph._node_edge_chain
   :noindex:

Data Types
==========

The package uses several common data types:

.. py:data:: ndtools.typing.Dict[str, Any]
   :noindex:

   Dictionary mapping string keys to any values, commonly used for node and edge attributes.

.. py:data:: ndtools.typing.Tuple[Path, Path, Path]
   :noindex:

   Tuple of three Path objects representing nodes, edges, and probabilities file paths.

.. py:data:: ndtools.typing.Optional[Dict[str, Any]]
   :noindex:

   Optional dictionary, commonly used for probability data which may be None.

Error Handling
==============

The package defines several custom exceptions:

.. exception:: ndtools.exceptions.ValidationError
   :noindex:

   Raised when data validation fails against JSON schemas.

.. exception:: ndtools.exceptions.FileNotFoundError
   :noindex:

   Raised when required dataset files are not found.

.. exception:: ndtools.exceptions.GraphConstructionError
   :noindex:

   Raised when graph construction fails due to invalid data.

Configuration
=============

The package can be configured through environment variables:

.. envvar:: NDTOOLS_CACHE_DIR
   :noindex:

   Directory for caching loaded datasets (default: ``~/.ndtools/cache``).

.. envvar:: NDTOOLS_LOG_LEVEL
   :noindex:

   Logging level for the package (default: ``INFO``).

.. envvar:: NDTOOLS_MAX_WORKERS
   :noindex:

   Maximum number of worker processes for parallel operations (default: ``4``).

Examples
========

Basic Usage
-----------

.. code-block:: python

   from ndtools.io import dataset_paths, load_json
   from ndtools.graphs import build_graph
   from pathlib import Path

   # Load a dataset
   nodes_path, edges_path, probs_path = dataset_paths(Path('.'), 'toynet-11edges', 'v1')
   nodes = load_json(nodes_path)
   edges = load_json(edges_path)
   probs = load_json(probs_path)
   
   # Build graph
   G = build_graph(nodes, edges, probs)

Advanced Usage
--------------

.. code-block:: python

   from ndtools.fun_binary_graph import eval_global_conn_k
   from ndtools.graphs import draw_graph_from_data
   import networkx as nx

   # Evaluate system performance
   comps_state = {"e1": 1, "e2": 0, "n1": 1}
   k_val, status, _ = eval_global_conn_k(comps_state, G, target_k=2)
   
   # Visualize with custom layout
   draw_graph_from_data(
       "dataset/v1/data",
       layout="kamada_kawai",
       layout_kwargs={"weight": "length"},
       with_edge_labels=True
   )

Performance Tips
================

* Use ``dataset_paths()`` to get file paths instead of hardcoding them
* Load data once and reuse the graph object for multiple analyses
* Use appropriate layout algorithms for visualization (``spring`` for small graphs, ``kamada_kawai`` for larger ones)
* Enable parallel processing for system function evaluation on large networks
