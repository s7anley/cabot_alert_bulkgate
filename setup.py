#!/usr/bin/env python

from setuptools import setup, find_packages

VERSION = '1.0.0'

setup(name='cabot-alert-bulkgate',
      version=VERSION,
      description='A Bulkgate SMS alert plugin for Cabot',
      url='http://cabotapp.com',
      packages=find_packages(),
      download_url='https://github.com/s7anley/cabot_alert_bulkgate/archive/{}.zip'.format(VERSION),
     )
