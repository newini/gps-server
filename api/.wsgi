#!/usr/bin/env python3
#.wsgi
# ================================
# Author: newini
# Date: April 2020
# Project: GPS server
# Description: WSGI for Flask API
# ================================


import sys
sys.path.insert(0, '/var/www/gps-server/api')

# Problem on loading lib64 packages, So, have to append lib64
sys.path.append('/usr/local/lib64/python3.6/site-packages')

# Clear arguments and Add arguments
sys.argv = ['']
# config path
sys.argv.append('--config')
sys.argv.append('/var/www/gps-server/api/my_configure.yml')

from app import app as application
