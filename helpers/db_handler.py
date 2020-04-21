#!/usr/bin/env python3
# db_handler.py
# ==============================
# Author: newini
# Date: April 2020
# Project: GPS server
# Description: DB handler
# ==============================


import sys

sys.path.append("..")
from helpers.app import *


import sqlite3

db = sqlite3.connect(config["db_path"], check_same_thread=False)
cursor = db.cursor()


# =================================
# DB devices
def createDevicesTable():
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS devices(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, imei TEXT UNIQUE, created_date TEXT, modified_date TEXT)"
    )
    db.commit()


def addDevice(name, imei):
    dummy = (
        name,
        imei,
        datetime.datetime.now(),
        datetime.datetime.now(),
    )
    cursor.execute(
        "INSERT INTO devices(name, imei, created_date, modified_date) VALUES(?, ?, ?, ?)",
        dummy,
    )
    db.commit()


def getDevice(imei):
    cursor.execute("SELECT * FROM devices WHERE imei = %s" % imei)
    rows = cursor.fetchall()
    if len(rows) > 0:
        device = {"name": rows[0][1], "imei": rows[0][2], "created_date": rows[0][3]}
        return device


def getDevices():
    cursor.execute("SELECT * FROM devices")
    rows = cursor.fetchall()
    if len(rows) > 0:
        devices = [
            {"name": row[1], "imei": row[2], "created_date": row[3]} for row in rows
        ]
        return devices


# =================================
# DB gps
def createGpsTable():
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS gps(id INTEGER PRIMARY KEY AUTOINCREMENT, imei TEXT, lat REAL, lng REAL, created_date TEXT)"
    )
    db.commit()


def addGps(imei, lat, lng):
    data = (
        imei,
        lat,
        lng,
        datetime.datetime.now(),
    )
    cursor.execute(
        "INSERT INTO gps(imei, lat, lng, created_date) VALUES(?, ?, ?, ?)", data
    )
    db.commit()


def getGps(imei):
    cursor.execute("SELECT * FROM gps WHERE imei = %s ORDER BY id DESC LIMIT 1" % imei)
    results = cursor.fetchall()
    coordinate = {"lat": results[0][2], "lng": results[0][3]}
    return coordinate


# =================================
# Drop
def dropDB():
    cursor.execute("DROP TABLE IF EXISTS devices")
    cursor.execute("DROP TABLE IF EXISTS gps")
    db.commit()
