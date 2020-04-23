#!/usr/bin/env python3
# app.py
# ==============================
# Author: newini
# Date: April 2020
# Project: GPS server
# Description: Websocket
# ==============================


import logging


class Websocket():
    def __init__(self, socketio, mongo):
        self.socketio       = socketio
        self.mongo          = mongo
        self.stop_signal    = False
        self.is_running     = False
        logging.info('[Websocket] initialized')


    def emitGpsData(self):
        self.is_running = True
        previous_gps_json = {}
        while True:
            if self.stop_signal:
                self.stop_signal = False
                self.is_running = False
                break

            devices = self.mongo.db.devices.find()

            for device in devices:
                gps_bson = self.mongo.db.coordinates.find_one({'imei': device['imei']})
                gps_json = {
                    'lat': gps_bson['lat'],
                    'lng': gps_bson['lng'],
                    'time': str(gps_bson['time']),
                        }

                if previous_gps_json != gps_json:
                    logging.info('[Websocket]: send' + str(gps_json))
                    self.socketio.emit('my response', gps_json)
                    previous_gps_json = gps_json

            self.socketio.sleep(5)


    def run(self):
        logging.info('[Websocket] run')
        if self.is_running:
            self.stop()
        self.emitGpsData()


    def stop(self):
        logging.info('[Websocket] stop')
        self.stop_signal = True
