#!/usr/bin/env python3
# app.py
# ==============================
# Author: newini
# Date: April 2020
# Project: GPS server
# Description: Flask API
# ==============================


# Defult packages
import os, sys

# Installed pakages
from flask import Flask, request, jsonify, abort
from flask_pymongo import PyMongo


# -------------------------------------
#       Arguments and configure
# -------------------------------------
def initializeConfigure():
    import argparse, yaml

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--config", help="Config file path", type=str, default="/var/www/gps-server/api/configure.yml"
    )
    args = parser.parse_args()

    # Load yml configure
    config_file = open(args.config, "r")
    config = yaml.safe_load(config_file)
    return config


# --------------------------------------
#               logging
# --------------------------------------
import os, datetime
import logging, coloredlogs
def initializeLogging(config):
    # Create log directory if need
    if len(config["logfile_dir"].split("/")) > 1:
        log_directory = config["logfile_dir"].rsplit("/", 1)[0]
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="%s/%s.log"
        % (config["logfile_dir"], datetime.datetime.now().strftime("%Y-%m-%d")),
        filemode="a",
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

    # color logging
    coloredlogs.install()


config = initializeConfigure()
initializeLogging(config)


# Application and PyMongo
app = Flask(__name__)
app.config['MONGO_URI'] = config['MONGO_URI']
mongo = PyMongo(app)


# =================================
#               API
# =================================
@app.route("/api", methods=["POST"])
def route_api():
    # Check token
    if request.headers.get("token") != config['GPS_SERVER_API_TOKEN']:
        logging.error("token not valid")
        abort(401)

    # Check json
    post_json = request.json
    logging.debug(post_json)
    if not "imei" in post_json:
        logging.error("imei not valid")
        abort(400)

    # Check device
    device = mongo.db.devices.find_one({'imei': post_json['imei']})
    if not device:
        logging.error("device not found")
        abort(500)

    logging.info("API: GPS data received. device: " + device['name'] + ", data: " + str(post_json))

    # Store data
    post_json['time'] = datetime.datetime.now()
    mongo.db.coordinates.insert(post_json)

    return jsonify({"status": "200"})


if __name__ == "__main__":
    app.run(config["host"], config["port"], debug=config["debug"])
