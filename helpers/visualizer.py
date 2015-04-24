#! /usr/bin/python
# coding: utf-8


def print_action_result(type, message):
    if type == "d":
        print "Package is sent"
        print "*----------------*"
        return

    if type == "v":
        print "Package is received"
        print "*----------------*"
        return

    if type == "r":
        print "Error: %s" % message
        print "*----------------*"
        return
