#!/usr/bin/env python3
# app_helper.py
# ==============================
# Author: newini
# Date: April 2020
# Project: GPS server
# Description: App helper
# ==============================


# -------------------------------------
#       Arguments and configure
# -------------------------------------
def initializeConfigure():
    import argparse, yaml

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--config", help="Config file path", type=str, default="configure.yml"
    )
    args = parser.parse_args()

    # Load yml configure
    config_file = open(args.config, "r")
    config = yaml.safe_load(config_file)
    return config


# --------------------------------------
#               logging
# --------------------------------------
import logging
def initializeLogging(config):
    import os, datetime
    import coloredlogs
    # Check if last character is '/'
    if config['logfile_dir_path'][-1] is not '/':
        config['logfile_dir_path'] = config['logfile_dir_path'] + '/'

    # Create log directory if need
    if len(config["logfile_dir_path"].split("/")) > 1:
        log_directory = config["logfile_dir_path"].rsplit("/", 1)[0]
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="%s/gps_server_viewer_%s.log"
        % (config["logfile_dir_path"], datetime.datetime.now().strftime("%Y%m")),
        filemode="a",
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

    # color logging
    coloredlogs.install()
