How to contribute
============

We welcome contributions to the Network Datasets repository! This page provides guidelines for contributing datasets, code improvements, and documentation.

Types of Contributions
----------------------

We accept several types of contributions:

* **New datasets**: Infrastructure network datasets following our format
* **Code improvements**: Bug fixes, new features, performance optimizations
* **Documentation**: Improvements to existing docs, new tutorials
* **Testing**: Additional test cases, validation improvements
* **Examples**: New Jupyter notebooks, usage examples

Getting Started
---------------

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:

   .. code-block:: bash

      git clone https://github.com/your-username/network-datasets.git
      cd network-datasets

3. **Create a development environment**:

   .. code-block:: bash

      conda create -n network-datasets-dev python=3.9
      conda activate network-datasets-dev
      pip install -e ".[dev]"

4. **Install pre-commit hooks** (optional but recommended):

   .. code-block:: bash

      pip install pre-commit
      pre-commit install

Adding New Datasets
-------------------

Dataset Structure
~~~~~~~~~~~~~~~~~

New datasets should follow this directory structure:

.. code-block:: text

   dataset-name/
   ├── dataset.yaml          # Dataset metadata
   └── v1/                   # Version directory
       ├── data/             # Data files
       │   ├── nodes.json    # Node definitions
       │   ├── edges.json    # Edge definitions
       │   └── probs.json    # Probability data
       ├── docs/             # Documentation
       │   ├── README.md     # Dataset description
       │   ├── PROVENANCE.md # Data source information
       │   └── CHANGELOG.md  # Version history
       └── scripts/          # Analysis scripts (optional)
           └── example.ipynb

Required Files
~~~~~~~~~~~~~~

**dataset.yaml**
   Dataset metadata file with the following structure:

   .. code-block:: yaml

      name: dataset-name
      version: 1.0.0
      title: Human-readable title
      license: CC-BY-4.0
      description: >
        Detailed description of the dataset including:
        - What type of infrastructure network
        - Number of nodes and edges
        - Data source and methodology
        - Use cases and applications
      contacts:
        - name: Your Name
          affiliation: Your Institution
          email: your.email@example.com
      tags: [power, transportation, water, etc.]
      files:
        nodes: data/nodes.json
        edges: data/edges.json
        probs: data/probs.json
      citation: |
        Citation information for the dataset

**nodes.json**
   Node definitions following the JSON schema:

   .. code-block:: json

      {
        "node_id": {
          "x": 0.0,
          "y": 0.0,
          "type": "optional_type",
          "additional_attributes": "optional"
        }
      }

**edges.json**
   Edge definitions following the JSON schema:

   .. code-block:: json

      {
        "edge_id": {
          "from": "node1",
          "to": "node2",
          "directed": false,
          "additional_attributes": "optional"
        }
      }

**probs.json**
   Probability data for edge failures:

   .. code-block:: json

      {
        "edge_id": {
          "1": {"p": 0.95},
          "0": {"p": 0.05}
        }
      }

Data Quality Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

* **Coordinates**: Use consistent units (e.g., kilometers) and coordinate system
* **Node IDs**: Use descriptive, unique identifiers
* **Edge IDs**: Use descriptive, unique identifiers
* **Attributes**: Include relevant metadata (capacity, type, etc.)
* **Probabilities**: Ensure probabilities sum to 1.0 for each edge
* **Validation**: All data must pass schema validation

Dataset Documentation
~~~~~~~~~~~~~~~~~~~~~

Create comprehensive documentation for your dataset:

**README.md**
   Include:
   * Dataset overview and purpose
   * Data source and methodology
   * Network statistics (nodes, edges, connectivity)
   * Usage examples
   * Citation information

**PROVENANCE.md**
   Include:
   * Original data source
   * Processing steps and transformations
   * Assumptions and limitations
   * Data quality notes

**CHANGELOG.md**
   Track changes and updates to the dataset.

Validation
~~~~~~~~~~

Before submitting, validate your dataset:

.. code-block:: bash

   # Validate all datasets
   python data_validate.py --root .

   # Validate specific dataset
   python data_validate.py --root . --dataset your-dataset-name

Update Registry
~~~~~~~~~~~~~~~

Add your dataset to the ``registry.json`` file:

.. code-block:: json

   [
     {
       "name": "your-dataset-name",
       "version": "1.0.0",
       "path": "your-dataset-name/v1",
       "summary": "Brief description of your dataset",
       "license": "CC-BY-4.0"
     }
   ]

Code Contributions
------------------

Code Style
~~~~~~~~~~

* Follow PEP 8 style guidelines
* Use type hints for function parameters and return values
* Write docstrings for all public functions
* Use meaningful variable and function names

Testing
~~~~~~~

* Write tests for new functionality
* Ensure all existing tests pass
* Aim for good test coverage

.. code-block:: bash

   # Run tests
   pytest tests/

   # Run with coverage
   pytest --cov=ndtools tests/

Documentation
~~~~~~~~~~~~~

* Update docstrings for modified functions
* Add examples to the documentation
* Update the API reference if needed

Pull Request Process
--------------------

1. **Create a feature branch**:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. **Make your changes** and commit them:

   .. code-block:: bash

      git add .
      git commit -m "Add your dataset: brief description"

3. **Push to your fork**:

   .. code-block:: bash

      git push origin feature/your-feature-name

4. **Create a pull request** on GitHub with:
   * Clear description of changes
   * Reference to any related issues
   * Screenshots for UI changes
   * Test results

Pull Request Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

* Keep PRs focused on a single feature or dataset
* Write clear, descriptive commit messages
* Respond to review feedback promptly
* Update documentation as needed
* Ensure all tests pass

Review Process
--------------

All contributions are reviewed by maintainers:

* **Code quality**: Style, functionality, tests
* **Data quality**: Validation, documentation, format compliance
* **Documentation**: Clarity, completeness, accuracy
* **Testing**: Coverage, correctness

Reviewers may request changes before merging.

License
-------

By contributing to this project, you agree that your contributions will be licensed under the same licenses as the project:

* **Code**: MIT License
* **Data**: CC-BY-4.0 License

This means your contributions can be used by others under these terms.

Getting Help
------------

If you need help with contributing:

* **Open an issue** on GitHub for questions
* **Check existing issues** for similar questions
* **Read the documentation** thoroughly
* **Ask in discussions** for general questions

Recognition
-----------

Contributors will be recognized in:

* The project's README.md file
* Release notes for significant contributions
* The project's documentation

Thank you for contributing to the Network Datasets project!
