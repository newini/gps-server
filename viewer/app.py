#!/usr/bin/env python3
# app.py
# ==============================
# Author: newini
# Date: April 2020
# Project: GPS server
# Description: Flask Viewer APP
# ==============================


# Installed packages
from flask import Flask, request, redirect, render_template
from flask_socketio import SocketIO
from flask_pymongo import PyMongo
from bson import json_util

# Helper
from helpers.app_helper import *

# Classes
#from classes.device import Device
from classes.Websocket import Websocket


# Load configure
config = initializeConfigure()
initializeLogging(config)


# Application
app = Flask(__name__)
app.config['MONGO_URI'] = config['MONGO_URI']
mongo = PyMongo(app)
socketio = SocketIO(app)


#=================================
#       page routing
#=================================
@app.route('/')
def route_index():
    return redirect("dashboard")


@app.route('/dashboard')
def route_dashboard():
    data = {'CATEGORY': 'live'}
    #return template("dashboard.html", data)
    devices = mongo.db.devices.find()
    return render_template("dashboard.html", GOOGLE_MAP_API_KEY = config['GOOGLE_MAP_API_KEY'], devices = devices)


@app.route('/manage')
def route_manage():
    data = {'CATEGORY': 'live'}
    return template("manage.html", data)


@app.route('/login')
def route_login():
    data = {'CATEGORY': 'live'}
    return template("login.html", data)


#=================================
#       Websocket
websocket_client = Websocket(socketio, mongo)

@socketio.on('server_connected')
def websocket_connected(json, methods=['GET', 'POST']):
    logging.info('[Websocket]: client connected')
    websocket_client.run()


@socketio.on('disconnect')
def websocket_disconnected():
    logging.info('[Websocket]: client disconnected')
    websocket_client.stop()


if __name__ == "__main__":
    socketio.run(app, host=config['host'], port=config['port'], debug=config['debug'])
