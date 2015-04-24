#! /usr/bin/python
# coding: utf-8

DATA = 'd'
COMMAND = 'c'
ERROR = 'r'
RECEIVE = 'v'


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
            return 1

        print "Handle Solar Panel Success"
        print "Solar panel pozitions:"
        print "Panel_1: %d degrees" % cls.solar_panel1_pozition
        print "Panel_2: %d degrees" % cls.solar_panel2_pozition
        print "*----------------*"

        RF.sp_Send(DATA, '1;1;s;%s;%s;success' % (cls.solar_panel1_pozition, cls.solar_panel2_pozition))

    @classmethod
    def get_solar_panel(cls, RF, payload):
        print "Get Solar Panel Success"
        print "Solar panel pozitions:"
        print "Panel_1: %d degrees" % cls.solar_panel1_pozition
        print "Panel_2: %d degrees" % cls.solar_panel2_pozition
        print "*----------------*"

        RF.sp_Send(DATA, '1;1;g;%s;%s;success' % (cls.solar_panel1_pozition, cls.solar_panel2_pozition))

    @classmethod
    def get_outer_temperature(cls, RF, payload):
        with open('sensors/outer_temperature') as f:
            cls.outer_temperature = int(f.read())

        print "Get Temperature Success"
        print "Outer temperature: %s K" % cls.outer_temperature

        RF.sp_Send(DATA, '1;1;o;%s;success' % cls.outer_temperature)

    @classmethod
    def get_telemetry(cls, RF, payload):
        print "Get Telemetry Success"
        print "*----------------*"

        RF.sp_Send(DATA, '1;1;t;telemetry;success')

commands = {
    's': Commands.handle_solar_panel,
    'g': Commands.get_solar_panel,
    't': Commands.get_telemetry,
    'o': Commands.get_outer_temperature
}