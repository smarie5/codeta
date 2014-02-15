CodeTA 1
======

A tool for automated source code grading.

Quick-start
===========
To install everything

> sudo ./deploy.sh all

Run unit tests

> python tests.py


Deployment Options
==================

To update server configuration from github

> sudo ./deploy.sh puppet

To install only the bootstrap puppet scripts

> sudo ./deploy.sh server

To install only the webapp

> sudo ./deploy.sh webapp
