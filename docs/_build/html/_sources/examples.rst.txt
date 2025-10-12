Examples
========

This page provides comprehensive examples demonstrating how to use the Network Datasets package for various network analysis tasks.

Basic Examples
--------------

Loading and Visualizing a Dataset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ndtools.io import dataset_paths, load_json
   from ndtools.graphs import build_graph, draw_graph_from_data
   from pathlib import Path

   # Load the toy network dataset
   nodes_path, edges_path, probs_path = dataset_paths(Path('.'), 'toynet-11edges', 'v1')
   
   # Load data
   nodes = load_json(nodes_path)
   edges = load_json(edges_path)
   probs = load_json(probs_path)
   
   # Build NetworkX graph
   G = build_graph(nodes, edges, probs)
   
   print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
   
   # Visualize the network
   output_path = draw_graph_from_data(
       "toynet-11edges/v1/data",
       layout="spring",
       with_node_labels=True,
       title="Toy Network Example"
   )
   
   print(f"Graph saved to: {output_path}")

Calculating Edge Lengths
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ndtools.graphs import compute_edge_lengths
   from ndtools.io import dataset_paths, load_json
   from pathlib import Path

   # Load dataset with spatial coordinates
   nodes_path, edges_path, probs_path = dataset_paths(Path('.'), 'ema-highway', 'v1')
   nodes = load_json(nodes_path)
   edges = load_json(edges_path)
   
   # Calculate edge lengths
   lengths = compute_edge_lengths(nodes, edges)
   
   # Display results
   for edge_id, length in lengths.items():
       print(f"Edge {edge_id}: {length:.2f} km")

System Function Evaluation
--------------------------

Global Connectivity Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ndtools.fun_binary_graph import eval_global_conn_k
   from ndtools.graphs import build_graph
   from ndtools.io import dataset_paths, load_json
   from pathlib import Path

   # Load dataset
   nodes_path, edges_path, probs_path = dataset_paths(Path('.'), 'toynet-11edges', 'v1')
   nodes = load_json(nodes_path)
   edges = load_json(edges_path)
   probs = load_json(probs_path)
   G = build_graph(nodes, edges, probs)
   
   # Define different failure scenarios
   scenarios = [
       {"name": "All working", "state": {"e1": 1, "e2": 1, "e3": 1, "e4": 1}},
       {"name": "One edge failed", "state": {"e1": 0, "e2": 1, "e3": 1, "e4": 1}},
       {"name": "Two edges failed", "state": {"e1": 0, "e2": 0, "e3": 1, "e4": 1}},
   ]
   
   # Evaluate each scenario
   for scenario in scenarios:
       k_val, state, _ = eval_global_conn_k(scenario["state"], G)
       print(f"{scenario['name']}: k={k_val}, System state={state}")

Travel Time Analysis
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ndtools.fun_binary_graph import eval_travel_time_to_nearest
   from ndtools.graphs import build_graph, compute_edge_lengths
   from ndtools.io import dataset_paths, load_json
   from pathlib import Path

   # Load highway dataset
   nodes_path, edges_path, probs_path = dataset_paths(Path('.'), 'ema-highway', 'v1')
   nodes = load_json(nodes_path)
   edges = load_json(edges_path)
   probs = load_json(probs_path)
   
   # Build graph
   G = build_graph(nodes, edges, probs)
   
   # Add length attributes to edges
   lengths = compute_edge_lengths(nodes, edges)
   for edge_id, length in lengths.items():
       if edge_id in G.edges():
           G.edges[edge_id]['length'] = length
   
   # Define origin and destinations
   origin = "n1"  # Replace with actual node ID
   destinations = ["n5", "n10", "n15"]  # Replace with actual node IDs
   
   # Evaluate travel time under different scenarios
   scenarios = [
       {"name": "Normal conditions", "state": {}},
       {"name": "Some roads closed", "state": {"e1": 0, "e2": 0}},
   ]
   
   for scenario in scenarios:
       time, state, info = eval_travel_time_to_nearest(
           scenario["state"], G, origin, destinations,
           avg_speed=60.0,  # km/h
           target_max=0.5,  # 30 minutes extra
           length_attr="length"
       )
       
       if time is not None:
           print(f"{scenario['name']}: {time:.2f} hours, system state={state}")
       else:
           print(f"{scenario['name']}: No path available, system state={state}")

Advanced Examples
-----------------

Monte Carlo Simulation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import random
   from ndtools.fun_binary_graph import eval_global_conn_k
   from ndtools.graphs import build_graph
   from ndtools.io import dataset_paths, load_json
   from pathlib import Path

   # Load dataset
   nodes_path, edges_path, probs_path = dataset_paths(Path('.'), 'toynet-11edges', 'v1')
   nodes = load_json(nodes_path)
   edges = load_json(edges_path)
   probs = load_json(probs_path)
   G = build_graph(nodes, edges, probs)
   
   # Extract edge failure probabilities
   edge_probs = {}
   for edge_id, prob_data in probs.items():
       if "0" in prob_data:  # Failure probability
           edge_probs[edge_id] = prob_data["0"]["p"]
   
   # Run Monte Carlo simulation
   n_simulations = 1000
   success_count = 0
   
   for _ in range(n_simulations):
       # Generate random component states
       comps_state = {}
       for edge_id, fail_prob in edge_probs.items():
           comps_state[edge_id] = 0 if random.random() < fail_prob else 1
       
       # Evaluate system performance
       k_val, state, _ = eval_global_conn_k(comps_state, G)
       if state < 2: # Example threshold of global connectivity as 2
           success_count += 1
   
   reliability = success_count / n_simulations
   print(f"System reliability: {reliability:.3f}")

Custom Visualisation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import matplotlib.pyplot as plt
   import networkx as nx
   from ndtools.graphs import build_graph
   from ndtools.io import dataset_paths, load_json
   from pathlib import Path

   # Load dataset
   nodes_path, edges_path, probs_path = dataset_paths(Path('.'), 'toynet-11edges', 'v1')
   nodes = load_json(nodes_path)
   edges = load_json(edges_path)
   probs = load_json(probs_path)
   G = build_graph(nodes, edges, probs)
   
   # Create custom visualization
   fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
   
   # Left plot: Normal conditions
   pos = nx.spring_layout(G)
   nx.draw(G, pos, ax=ax1, with_labels=True, node_color='lightblue', 
           node_size=500, font_size=8)
   ax1.set_title("Normal Conditions")
   
   # Right plot: With edge failures
   failed_edges = ["e1", "e2"]  # Example failed edges
   G_failed = G.copy()
   G_failed.remove_edges_from([(u, v) for u, v, d in G.edges(data=True) 
                              if d.get('eid') in failed_edges])
   
   nx.draw(G_failed, pos, ax=ax2, with_labels=True, node_color='lightcoral',
           node_size=500, font_size=8)
   ax2.set_title("With Edge Failures")
   
   plt.tight_layout()
   plt.savefig("custom_visualization.png", dpi=300)
   plt.show()

Data Validation
~~~~~~~~~~~~~~~

.. code-block:: python

   import jsonschema
   from ndtools.io import load_json
   from pathlib import Path

   def validate_dataset(dataset_path):
       """Validate a dataset against JSON schemas."""
       data_path = Path(dataset_path) / "v1" / "data"
       
       # Load schemas
       with open("schema/nodes.schema.json") as f:
           nodes_schema = json.load(f)
       with open("schema/edges.schema.json") as f:
           edges_schema = json.load(f)
       with open("schema/probs.schema.json") as f:
           probs_schema = json.load(f)
       
       # Load and validate data
       try:
           nodes = load_json(data_path / "nodes.json")
           jsonschema.validate(nodes, nodes_schema)
           print("✓ Nodes data is valid")
           
           edges = load_json(data_path / "edges.json")
           jsonschema.validate(edges, edges_schema)
           print("✓ Edges data is valid")
           
           probs = load_json(data_path / "probs.json")
           jsonschema.validate(probs, probs_schema)
           print("✓ Probabilities data is valid")
           
           return True
       except jsonschema.ValidationError as e:
           print(f"✗ Validation error: {e}")
           return False
       except FileNotFoundError as e:
           print(f"✗ File not found: {e}")
           return False

   # Validate all datasets
   datasets = ["toynet-11edges", "distribution-substation-liang2022", "ema-highway"]
   for dataset in datasets:
       print(f"\nValidating {dataset}:")
       validate_dataset(dataset)


Jupyter Notebook Examples
-------------------------

The repository includes several Jupyter notebooks with interactive examples:

* ``distribution_substation_liang2022/v1/scripts/demo_sys_fun.ipynb`` - Evaluation of a subsystem network's maximum capacity
* ``distribution_substation_liang2022/v1/scripts/demo_edge_prob_update.ipynb`` - Failure probability updates of edges, provided a peak ground acceleration (PGA) value
* ``ema_highway/v1/scripts/add_edge_attrs.ipynb`` - Adding lengths as edge attributes for network evaluation purposes
