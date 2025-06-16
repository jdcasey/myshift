Welcome to myshift's documentation!
================================

myshift is a command-line tool for managing PagerDuty on-call schedules. It provides functionality for viewing, planning, and overriding on-call shifts.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api
   configuration
   contributing

Installation
-----------

To install myshift, use pip:

.. code-block:: bash

   pip install myshift

Quick Start
----------

1. Create a configuration file:

.. code-block:: bash

   myshift config --print > ~/.config/myshift.yaml

2. Edit the configuration file with your PagerDuty API token and other settings.

3. Start using myshift:

.. code-block:: bash

   # View your next shift
   myshift next

   # View all upcoming shifts
   myshift upcoming

   # View the entire schedule
   myshift plan

   # Override a shift
   myshift override --start-date 2024-03-01 --target-user-email someone@example.com

Features
--------

* View upcoming on-call shifts
* Plan and view entire schedules
* Override shifts when needed
* Interactive REPL for quick access
* Configurable through YAML configuration

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 