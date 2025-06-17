Configuration
=============

This section details the configuration options available in myshift.

Configuration File
----------------

The configuration file is stored in YAML format and contains settings for the PagerDuty API connection and display preferences.

Configuration Options
-------------------

PagerDuty Settings
~~~~~~~~~~~~~~~~~

The following settings are required for connecting to the PagerDuty API:

* ``api_key``: Your PagerDuty API key
* ``schedule_id``: The ID of your on-call schedule

Display Settings
~~~~~~~~~~~~~~

The following settings control how information is displayed:

* ``timezone``: Your local timezone (e.g., "America/New_York")
* ``display_format``: Output format (default, json, or yaml)

Logging Settings
~~~~~~~~~~~~~~

The following settings control logging behavior:

* ``log_level``: Logging level (DEBUG, INFO, WARNING, ERROR)
* ``log_file``: Path to log file (optional)

Example Configuration
-------------------

Here's an example configuration file:

.. code-block:: yaml

   # PagerDuty Settings
   api_key: your_api_key_here
   schedule_id: your_schedule_id_here

   # Display Settings
   timezone: America/New_York
   display_format: default

   # Logging Settings
   log_level: INFO
   log_file: ~/.myshift/myshift.log

Environment Variables
-------------------

The following environment variables can be used to override configuration settings:

* ``Myshift_API_KEY``: PagerDuty API key
* ``Myshift_SCHEDULE_ID``: Schedule ID
* ``Myshift_TIMEZONE``: Timezone
* ``Myshift_DISPLAY_FORMAT``: Display format
* ``Myshift_LOG_LEVEL``: Log level
* ``Myshift_LOG_FILE``: Log file path

Configuration Management
----------------------

View Configuration
~~~~~~~~~~~~~~~~

To view your current configuration:

.. code-block:: bash

   myshift config show

Edit Configuration
~~~~~~~~~~~~~~~~

To edit your configuration:

.. code-block:: bash

   myshift config edit

Print Configuration
~~~~~~~~~~~~~~~~~

To print your configuration in a specific format:

.. code-block:: bash

   myshift config print --format json

Configuration Validation
----------------------

The configuration is validated when the application starts. The following checks are performed:

* Required settings are present
* API key is valid
* Schedule ID exists
* Timezone is valid
* Display format is supported
* Log level is valid

Best Practices
-------------

* Keep your API key secure and never commit it to version control
* Use environment variables for sensitive information
* Set an appropriate log level for your needs
* Use a valid timezone string from the IANA timezone database 