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
import argparse, yaml

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "--config", help="Config file path", type=str, default="configure.yml"
)
args = parser.parse_args()

# Load yml configure
config_file = open(args.config, "r")
config = yaml.safe_load(config_file)


# --------------------------------------
#               logging
# --------------------------------------
import datetime
import logging, coloredlogs

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
