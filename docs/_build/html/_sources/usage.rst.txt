Usage
=====

Basic Commands
-------------

View Next Shift
~~~~~~~~~~~~~~

To view your next scheduled shift:

.. code-block:: bash

   myshift next

Options:
* ``--schedule-id``: Specify a schedule ID
* ``--user-id``: Filter by user ID
* ``--user-email``: Filter by user email

View Upcoming Shifts
~~~~~~~~~~~~~~~~~~

To view your upcoming shifts:

.. code-block:: bash

   myshift upcoming

Options:
* ``--schedule-id``: Specify a schedule ID
* ``--weeks``: Number of weeks to look ahead (default: 4)
* ``--user-id``: Filter by user ID
* ``--user-email``: Filter by user email

View Schedule
~~~~~~~~~~~

To view the entire schedule:

.. code-block:: bash

   myshift plan

Options:
* ``--schedule-id``: Specify a schedule ID
* ``--weeks``: Number of weeks to look ahead (default: 4)
* ``--format``: Output format (default, json, yaml)

Override Shifts
~~~~~~~~~~~~~

To override a shift:

.. code-block:: bash

   myshift override --start "2024-03-01 09:00" --end "2024-03-02 09:00" --user-id "P123456"

Options:
* ``--schedule-id``: Specify a schedule ID
* ``--start``: Start time (required)
* ``--end``: End time (required)
* ``--user-id``: User ID to override with (required)
* ``--delete``: Delete an override instead of creating one

Configuration
------------

View Current Configuration
~~~~~~~~~~~~~~~~~~~~~~~

To view your current configuration:

.. code-block:: bash

   myshift config show

Options:
* ``--format``: Output format (default, json, yaml)

Interactive Mode
--------------

You can also use myshift in interactive mode:

.. code-block:: bash

   myshift

This starts an interactive shell with the following commands:

* ``next``: View next shift
* ``upcoming``: View upcoming shifts
* ``plan``: View schedule
* ``override``: Override a shift
* ``config``: View configuration
* ``help``: Show help
* ``exit``: Exit the shell

Example session:

.. code-block:: text

   $ myshift
   Welcome to myshift interactive shell
   Type 'help' for a list of commands
   
   myshift> next
   Your next shift is on 2024-03-01 09:00 - 2024-03-02 09:00
   
   myshift> upcoming
   Upcoming shifts:
   2024-03-01 09:00 - 2024-03-02 09:00
   2024-03-08 09:00 - 2024-03-09 09:00
   2024-03-15 09:00 - 2024-03-16 09:00
   
   myshift> exit
   Goodbye!

Tips and Tricks
--------------

1. Use the ``--format json`` option for machine-readable output:

   .. code-block:: bash

      myshift next --format json

2. Use the ``--weeks`` option to look further ahead:

   .. code-block:: bash

      myshift upcoming --weeks 8

3. Use the interactive mode for quick access to all commands:

   .. code-block:: bash

      myshift

For more detailed information about the API and configuration options, see the :doc:`api` and :doc:`configuration` documentation. 