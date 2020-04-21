#!/usr/bin/env python3
# app.py
# ==============================
# Author: newini
# Date: April 2020
# Project: GPS server
# Description: API
# ==============================


# Defult packages
import os, sys

# Installed pakages
from flask import Flask, request, jsonify


# Import helpers
sys.path.append("..")
from helpers.app import *
from helpers.db_handler import *


# Application
app = Flask(__name__)


# Env
GPS_SERVER_API_TOKEN = os.getenv("GPS_SERVER_API_TOKEN")


# =================================
#               API
# =================================
@app.route("/api", methods=["POST"])
def route_api():
    # Check token
    if request.headers.get("token") != GPS_SERVER_API_TOKEN:
        logging.error("token not valid")
        abort(401)

    # Check json
    post_json = request.json
    print(post_json)
    if not "imei" in post_json:
        logging.error("imei not valid")
        abort(400)

    # Check device
    device = getDevice(post_json["imei"])
    if not device:
        logging.error("device not found")
        abort(500)

    logging.info("API: received from " + device["name"] + ", data: " + str(post_json))

    # Store data
    addGps(post_json["imei"], post_json["lat"], post_json["lng"])

    return jsonify({"status": "200"})


if __name__ == "__main__":
    app.run(config["host"], config["port"], debug=config["debug"])
