==========================
Random Network Generator (ndtools)
==========================

``ndtools.network_generator`` creates synthetic network datasets (nodes, edges, probabilities)
that conform to this repo’s schemas. It can also draw a quick preview figure.

Example generated datasets are available under::

  generated/<name>/v1/
    data/
      nodes.json
      edges.json
      probs.json
      graph.png         (if plotting enabled)
    README.md
    metadata.json

.. note::

   Run commands from the **repo root** so that ``ndtools`` and ``schema/`` are found.

Quick Start (Windows cmd)
=========================

Activate your environment and change to the repo folder:

.. code-block:: cmd

   conda activate mbnpy_dev
   cd C:\Users\jb622s\git\network-datasets

Examples
========

Grid (8×8)
----------

.. code-block:: cmd

   python -m ndtools.network_generator ^
     --type grid ^
     --name grid_8x8 ^
     --rows 8 ^
     --cols 8 ^
     --p_fail 0.1 ^
     --description "8x8 grid demo"

Erdős–Rényi (ER)
----------------

.. code-block:: cmd

   python -m ndtools.network_generator ^
     --type erdos_renyi ^
     --name er_60_p005 ^
     --n_nodes 60 ^
     --p 0.05 ^
     --p_fail 0.05 ^
     --description "ER(60,0.05) demo" --seed 7

Watts–Strogatz (WS)
-------------------

.. code-block:: cmd

   python -m ndtools.network_generator ^
     --type ws ^
     --name ws_n60_k6_b015 ^
     --n_nodes 60 ^
     --k 6 ^
     --p_ws 0.15 ^
     --p_fail 0.1 ^
     --seed 7 ^
     --description "Watts–Strogatz graph, n=60, k=6, beta=0.15"

Random Geometric (RG)
---------------------

.. code-block:: cmd

   python -m ndtools.network_generator ^
     --type rg ^
     --name rg_n60_r017 ^
     --n_nodes 60 ^
     --radius 0.17 ^
     --p_fail 0.1 ^
     --seed 7 ^
     --description "Random geometric graph, n=60, r=0.17 (~150 edges)"

Configuration (average degree)
------------------------------

.. code-block:: cmd

   python -m ndtools.network_generator ^
     --type config ^
     --name config_n60_deg3 ^
     --n_nodes 60 ^
     --avg_deg 3 ^
     --p_fail 0.1 ^
     --seed 7 ^
     --description "Configuration model, n=60, avg_deg=3"

Barabási–Albert (BA)
--------------------

.. code-block:: cmd

   python -m ndtools.network_generator ^
     --type ba ^
     --name ba_n60_m3 ^
     --n_nodes 60 ^
     --m 3 ^
     --p_fail 0.1 ^
     --seed 7 ^
     --description "Barabasi-Albert, n=60, m=3 (~174 edges)"

What Gets Generated
===================

``nodes.json`` (dict)
   ``{"n0": {"x": <float|null>, "y": <float|null>}, ...}``

   * Grid assigns integer lattice coordinates (``x = i % cols``, ``y = i // cols``).
   * ER / WS / BA / Config set ``x,y`` to ``null`` (no embedded coordinates).
   * RG sets positions from the unit-square coordinates used to build the graph.

``edges.json`` (dict)
   ``{"e0": {"from": "n0", "to": "n1", "directed": false}, ...}``

``probs.json`` (dict)
   Binary edge state probabilities (failure/survival) per edge id::

     {
       "e0": {"0": {"p": 0.1}, "1": {"p": 0.9}},
       ...
     }

``graph.png`` (optional)
   A preview figure rendered by :func:`ndtools.graphs.draw_graph_from_data`.
   If nodes have numeric ``x,y`` (e.g., RG, Grid), those are used; otherwise a layout is computed.

CLI Arguments
=============

Common
------

``--type {grid,lattice,erdos_renyi|er,watts_strogatz|ws,barabasi_albert|ba,configuration|config,random_geometric|rg}``

``--name`` (str)
   Dataset folder name (used under ``generated/``).

``--description`` (str)
   Human-readable description written to ``README.md`` / ``metadata.json``.

``--p_fail`` (float)
   Edge failure probability. Survival is ``1 - p_fail``.

``--seed`` (int)
   Random seed for reproducibility (where applicable).

Model-specific
--------------

Grid
  ``--rows`` (int), ``--cols`` (int)

ER
  ``--n_nodes`` (int), ``--p`` (float edge probability)

WS
  ``--n_nodes`` (int), ``--k`` (even int), ``--p_ws`` (rewiring probability β)

BA
  ``--n_nodes`` (int), ``--m`` (int edges per new node)

Configuration
  ``--n_nodes`` (int), ``--avg_deg`` (float average degree to target)

Random Geometric
  ``--n_nodes`` (int), ``--radius`` (float in [0,1])

Notes on Edge Counts
====================

- **ER**: expected edges :math:`E \approx p \cdot \frac{n(n-1)}{2}`.
- **WS**: edges fixed by ``k``: :math:`E = \frac{n k}{2}` (β changes structure, not count).
- **BA**: edges fixed by ``m``: :math:`E = m n - \frac{m(m+1)}{2}`.
- **RG**: edges grow roughly with :math:`r^2`; tune ``--radius`` (e.g., ``0.17`` for ~150 edges at ``n=60``).
- **Config**: edges follow the synthesized degree sequence; ``avg_deg`` ≈ ``2E/n``.

Validation & Preview
====================

After generation, the tool:

1. Writes JSON files under ``generated/<name>/v1/data``.
2. Validates them against repo schemas in ``schema/``.
3. Optionally draws a preview figure (``graph.png``) using :mod:`ndtools.graphs`.

Troubleshooting
===============

- **“required arguments” errors**: You’re missing one of the required flags for that generator (see *Model-specific*).
- **WS: k must be even**: The tool adjusts ``k`` to be even (and ``< n``), but prefer to pass a valid value.
- **RG too many/few edges**: Adjust ``--radius`` slightly (e.g., ``0.15`` fewer, ``0.20`` more at ``n=60``).
- **Config avg degree**: For a target of ~95 edges at ``n=60``, use ``--avg_deg ~ 3.167``.

Programmatic Use
================

You can call the generator from Python:

.. code-block:: python

   from pathlib import Path
   from ndtools.network_generator import GenConfig, generate_and_save

   cfg = GenConfig(
       name="ws_n60_k6_b015",
       generator="ws",
       description="WS n=60 k=6 beta=0.15",
       generator_params={"n_nodes": 60, "k": 6, "p_ws": 0.15, "p_fail": 0.1},
       seed=7,
   )
   repo_root = Path(__file__).resolve().parents[1]
   out_base = repo_root / "generated"
   schema_dir = repo_root / "schema"

   ds_root = generate_and_save(out_base, schema_dir, cfg, draw_graph=True)
   print("Wrote:", ds_root)

Acknowledgments
===============

The network generator extensions were drafted by **`Alex Sixie Cao <https://scholar.google.com/citations?user=QUu8BdEAAAAJ&hl=en>`_**.
