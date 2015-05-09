#! /usr/bin/python
# coding: utf-8
import time

from sp_kernel import ser

DATA = 'd'
COMMAND = 'c'
ERROR = 'r'
SUCCESS = 's'


class Commands():
    solar_panel1_pozition = 0
    solar_panel2_pozition = 0
    outer_temperature = None

    @classmethod
    def handle_solar_panel(cls, RF, payload):
        cls.solar_panel1_pozition = int(payload[0])
        cls.solar_panel2_pozition = int(payload[1])

        if cls.solar_panel1_pozition < 0 or cls.solar_panel1_pozition > 90 \
                or cls.solar_panel2_pozition < 0 or cls.solar_panel2_pozition > 90:
            RF.sp_Send(ERROR, '1;1;s;%s;%s;invalid_param' % (cls.solar_panel1_pozition, cls.solar_panel2_pozition))
            print "Handle Solar Panel Error: invalid parameters"
            print "*----------------*"
            return 1

        print "Handle Solar Panel Success"
        print "Solar panel pozitions:"
        print "Panel_1: %d degrees" % cls.solar_panel1_pozition
        print "Panel_2: %d degrees" % cls.solar_panel2_pozition
        print "*----------------*"

        RF.sp_Send(SUCCESS, '1;1;s;%s;%s;success' % (cls.solar_panel1_pozition, cls.solar_panel2_pozition))

    @classmethod
    def get_solar_panel(cls, RF, payload):
        print "Get Solar Panel Success"
        print "Solar panel pozitions:"
        print "Panel_1: %d degrees" % cls.solar_panel1_pozition
        print "Panel_2: %d degrees" % cls.solar_panel2_pozition
        print "*----------------*"

        RF.sp_Send(SUCCESS, '1;1;g;%s;%s;success' % (cls.solar_panel1_pozition, cls.solar_panel2_pozition))

    @classmethod
    def get_outer_temperature(cls, RF, payload):
        with open('sensors/outer_temperature') as f:
            cls.outer_temperature = int(f.read())

        print "Get Temperature Success"
        print "Outer temperature: %s K" % cls.outer_temperature
        print "*----------------*"

        RF.sp_Send(SUCCESS, '1;1;o;%s;success' % cls.outer_temperature)

    @classmethod
    def get_telemetry(cls, RF, payload):
        print "Get Telemetry Success"
        print "*----------------*"

        RF.sp_Send(SUCCESS, '1;1;t;telemetry;success')

    @classmethod
    def satellite_activate(cls, RF, payload):
        print "Satellite activated"
        print "*----------------*"

        RF.sp_Send(SUCCESS, '1;1;satellite;activated;success')

    @classmethod
    def satllite_shutdown(cls, RF, payload):
        print "Settelite Sut Down"
        print "*----------------*"

        RF.sp_Send(SUCCESS, '1;1;satllite;shutdown;success')

    @classmethod
    def transceiver_state(cls, RF, payload):
        print "Get transceiver state"
        print "*----------------*"
        ser.write("+++")
        time.sleep(0.2)
        time.sleep(0.2)
        ser.write("ATS200?")
        time.sleep(0.2)
        ser.write("ATO\r")
        time.sleep(0.2)
        data = ser.readall()

        print "data: %s" % data

commands = {
    'a': Commands.satellite_activate,
    'b': Commands.satllite_shutdown,
    'c': Commands.transceiver_state,
    's': Commands.handle_solar_panel,
    'g': Commands.get_solar_panel,
    't': Commands.get_telemetry,
    'o': Commands.get_outer_temperature
}