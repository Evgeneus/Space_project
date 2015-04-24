#! /usr/bin/python
# coding: utf-8


class Commands():
    solar_panel1_pozition = 0
    solar_panel2_pozition = 0

    @classmethod
    def handle_solar_panel(cls, RF, payload):
        cls.solar_panel1_pozition = int(payload[0])
        cls.solar_panel2_pozition = int(payload[1])

        if cls.solar_panel1_pozition < 0 or cls.solar_panel1_pozition > 90 \
                or cls.solar_panel2_pozition < 0 or cls.solar_panel2_pozition > 90:
            RF.sp_Send('r', '1;1;s;%s;%s;invalid_param' % (cls.solar_panel1_pozition, cls.solar_panel2_pozition))
            print "Handle Solar Panel Error: invalid parameters"
            return 1

        print "Handle Solar Panel Success"
        print "Solar panel pozitions:"
        print "Panel_1: %d degrees" % cls.solar_panel1_pozition
        print "Panel_2: %d degrees" % cls.solar_panel2_pozition
        print "----------------"

        RF.sp_Send('d', '1;1;s;%s;%s;success' % (cls.solar_panel1_pozition, cls.solar_panel2_pozition))

    @classmethod
    def get_solar_panel(cls, RF, payload):
        print "Get Solar Panel Success"
        print "Solar panel pozitions:"
        print "Panel_1: %d degrees" % cls.solar_panel1_pozition
        print "Panel_2: %d degrees" % cls.solar_panel2_pozition
        print "----------------"

        RF.sp_Send('d', '1;1;g;%s;%s;success' % (cls.solar_panel1_pozition, cls.solar_panel2_pozition))

    @classmethod
    def get_telemetry(cls, RF, payload):
        print "Get telemetry"
        print payload

commands = {
    's': Commands.handle_solar_panel,
    'g': Commands.get_solar_panel,
    't': Commands.get_telemetry
}