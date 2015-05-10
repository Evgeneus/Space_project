#! /usr/bin/python
# coding: utf-8

from apscheduler.scheduler import Scheduler
import kernel.sp_kernel as sp_kernel
from kernel.commands import commands
from helpers.visualizer import print_action_result

DATA = 'd'
COMMAND = 'c'
ERROR = 'r'
SUCCESS = 's'

enable_transmission_flag = True
nomenal_mode_flag = False
operating_mode_flag = False
emergency_mode_flag = False


def handle_sattelite(package_info):
    global enable_transmission_flag
    global nomenal_mode_flag
    global operating_mode_flag
    global emergency_mode_flag
    global sched

    if not package_info['package_type'] == COMMAND\
            and not package_info['package_type'] == DATA\
            and not package_info['package_type'] == ERROR:
        print_action_result(ERROR, '%s not valid package_type' % package_info['package_type'])
        RF.sp_Send(ERROR, '%s not valid package_type' % package_info['package_type'])
        return 1

    if package_info['package_type'] == DATA:
        return

    if package_info['package_type'] == ERROR:
        print "ERROR"
        return

    payload = package_info['payload'].split(';')

    if len(payload) < 2:
        print_action_result(ERROR, 'package structure error')
        RF.sp_Send(ERROR, 'package structure error')
        return 1

    command_type = payload[2]
    if command_type == 'q':
        command = set_nomenal_mode
    elif command_type == 'z':
        command = set_operating_mode
    elif command_type == 'm':
        command = set_emergency_mode
    else:
        command = commands.get(command_type, None)

    if (not command) or (int(payload[0]) > int(payload[1])):
        print_action_result(ERROR, 'no command or package structure error')
        RF.sp_Send(ERROR, 'no command %s' % package_info['payload'])
        return 1

    if command_type == 'a':
        enable_transmission_flag = True
        command(RF, payload=payload[3:])
        return

    if command_type == 'b':
        enable_transmission_flag = False
        command(RF, payload=payload[3:])
        if nomenal_mode_flag or operating_mode_flag:
            sched.unschedule_func(beacon)
            nomenal_mode_flag = False
            operating_mode_flag = False
        else:
            sched.unschedule_func(beacon_emergency)
            emergency_mode_flag = False
        return

    if enable_transmission_flag:
        command(RF, payload=payload[3:])


def beacon():
    with open('sensors/outer_temperature') as f:
            outer_temperature = int(f.read())
    data = '1;1;TCPU;500;U;12;RAM;75;T;%s' %outer_temperature
    RF.sp_Send(DATA, data)
    print "Beacon sent"
    print "*----------------*"


def beacon_emergency():
    RF.sp_Send(DATA, '1;1;TCPU;500;U;12;RAM;75')
    print "Beacon Emergency Sent"
    print "*----------------*"


def set_nomenal_mode(RF, payload):
    global emergency_mode_flag
    global operating_mode_flag
    global nomenal_mode_flag

    if emergency_mode_flag:
        sched.unschedule_func(beacon_emergency)
        emergency_mode_flag = False
    elif operating_mode_flag:
        sched.unschedule_func(beacon)
        operating_mode_flag = False
    elif nomenal_mode_flag:
        sched.unschedule_func(beacon)

    if payload != []:
        delay = int(payload[0])
    else:
        delay = 15
    sched.add_interval_job(beacon, seconds=delay)
    nomenal_mode_flag = True
    RF.sp_Send(SUCCESS, '1;1;q')


    print "Set Nomenal Mode: %i seconds" % delay
    print "*----------------*"


def set_operating_mode(RF, payload):
    global emergency_mode_flag
    global nomenal_mode_flag
    global operating_mode_flag

    if emergency_mode_flag:
        sched.unschedule_func(beacon_emergency)
        emergency_mode_flag = False
    elif nomenal_mode_flag:
        sched.unschedule_func(beacon)
        nomenal_mode_flag = False
    elif operating_mode_flag:
        sched.unschedule_func(beacon)

    if payload != []:
        delay = int(payload[0])
    else:
        delay = 15
    sched.add_interval_job(beacon, seconds=delay)
    operating_mode_flag = True
    RF.sp_Send(SUCCESS, '1;1;z')

    print "Set Operating Mode: %i seconds" % delay
    print "*----------------*"


def set_emergency_mode(RF, payload):
    global emergency_mode_flag
    global operating_mode_flag
    global nomenal_mode_flag

    if nomenal_mode_flag:
        sched.unschedule_func(beacon)
        nomenal_mode_flag = False
    if operating_mode_flag:
        sched.unschedule_func(beacon)
        operating_mode_flag = False

    if payload != []:
        delay = int(payload[0])
    else:
        delay = 60
    sched.add_interval_job(beacon_emergency, seconds=delay)
    emergency_mode_flag = True
    RF.sp_Send(SUCCESS, '1;1;m')

    print "Set Operating Mode: %i seconds" % delay
    print "*----------------*"

if __name__ == "__main__":
    print "Initial protocol"
    RF = sp_kernel.SerialProtocol()

    sched = Scheduler()
    sched.start()
    sched.add_interval_job(beacon_emergency, seconds=60)
    emergency_mode_flag = True
    print "Set Emergency Mode"
    print "----------------"

    print "Start monitoring"
    print "----------------"

    while True:
        if sp_kernel.ser.inWaiting():
            if RF.sp_packetAvailable:
                RF.sp_packetAvailable = False
            package_info = RF.sp_Read()

            if package_info:
                handle_sattelite(package_info)
                print "monitoring ..."
