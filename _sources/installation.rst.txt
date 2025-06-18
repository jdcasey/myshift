Installation
============

Requirements
-----------

* Python 3.8 or higher
* pip (Python package installer)
* A PagerDuty account with API access

Installing from PyPI
------------------

The recommended way to install myshift is using pip:

.. code-block:: bash

   pip install myshift

This will install the latest stable version from PyPI.

Installing from Source
--------------------

To install from source:

1. Clone the repository:

.. code-block:: bash

   git clone https://github.com/yourusername/myshift.git
   cd myshift

2. Create a virtual environment:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate  # Windows

3. Install the package:

.. code-block:: bash

   pip install -e .

Configuration
------------

After installation, you need to configure myshift:

1. Create a configuration directory:

.. code-block:: bash

   mkdir -p ~/.config/myshift

2. Create a configuration file:

.. code-block:: bash

   myshift config --print > ~/.config/myshift/config.yaml

3. Edit the configuration file with your settings:

.. code-block:: yaml

   api_key: your_api_key_here
   schedule_id: your_schedule_id_here

Verifying Installation
--------------------

To verify your installation:

1. Check the version:

.. code-block:: bash

   myshift --version

2. Test the connection:

.. code-block:: bash

   myshift next

Troubleshooting
--------------

Common installation issues:

1. Permission denied when creating directories
   * Solution: Use sudo or check directory permissions

2. Module not found errors
   * Solution: Ensure you're in the correct virtual environment

3. Configuration file not found
   * Solution: Create the configuration directory and file

4. API connection errors
   * Solution: Verify your API key and schedule ID

For more help, see the :doc:`usage` guide or check the :doc:`api` documentation. 