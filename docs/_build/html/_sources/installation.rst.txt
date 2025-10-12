Installation
============

Requirements
------------

* Python >= 3.9
* NetworkX >= 3.0
* PyYAML >= 6.0
* jsonschema >= 4.0

Optional dependencies for visualization:
* matplotlib >= 3.0

Installation Methods
--------------------

Using pip (Editable Install)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From the repository root:

.. code-block:: bash

   # First activate your conda environment (if using conda)
   conda activate <your-env>

   # Then install in editable mode
   pip install -e .

This makes the ``ndtools`` package importable anywhere in that environment.

Using pip (Regular Install)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install ndtools

Verify Installation
-------------------

Check that the package is properly installed:

.. code-block:: bash

   python -c "import ndtools; print(ndtools.__version__)"

Run Tests
---------

To verify everything is working correctly:

.. code-block:: bash

   pytest -q

Development Installation
------------------------

For development work, you may want to install additional dependencies:

.. code-block:: bash

   # Install with development dependencies
   pip install -e ".[dev]"

   # Or install additional packages manually
   pip install pytest matplotlib jupyter

Environment Setup
~~~~~~~~~~~~~~~~~

For a clean environment setup:

.. code-block:: bash

   # Create new conda environment
   conda create -n network-datasets python=3.12
   conda activate network-datasets

   # Install the package
   pip install -e .

   # Verify installation
   python -c "import ndtools; print('Installation successful!')"
