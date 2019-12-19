Cabot Bulkgate Alert Plugin
=====

This is an alert plugin for the cabot service monitoring tool. It allows you to alert users by SMS.

## Installation

Install using pip

    pip install --no-cache-dir git+https://github.com/s7anley/cabot_alert_bulkgate.git

Edit `conf/production.env` in your Cabot clone to include the plugin:

    CABOT_PLUGINS_ENABLED=cabot_alert_bulkgate...,<other plugins>

## Configuration

The plugin requires the following environment variables to be set:

    BULKGATE_APP_ID=
    BULKGATE_APP_TOKEN=
