#! /usr/bin/python
# coding: utf-8


def handle_solar_panel(RF, payload):
    print "handle_solar_panel"
    print payload


def get_telemetry(RF, payload):
    print "get_telemetry"
    print payload

commands = {
    's': handle_solar_panel,
    't': get_telemetry
}