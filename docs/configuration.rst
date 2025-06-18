Configuration
=============

This section details the configuration options available in myshift.

Configuration File
-----------------

The configuration file is stored in YAML format and contains settings for the PagerDuty API connection.

Configuration Options
--------------------

PagerDuty Settings
~~~~~~~~~~~~~~~~~~

The following settings are required for connecting to the PagerDuty API:

* ``api_key``: Your PagerDuty API key
* ``schedule_id``: The ID of your on-call schedule

Example Configuration
---------------------

Here's an example configuration file:

.. code-block:: yaml

   # PagerDuty Settings
   api_key: your_api_key_here
   schedule_id: your_schedule_id_here

Configuration Validation
-----------------------

The configuration is validated when the application starts. The following checks are performed:

* Required settings are present
* API key is valid
* Schedule ID exists

Best Practices
--------------

* Keep your API key secure and never commit it to version control
