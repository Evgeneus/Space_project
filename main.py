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


def handle_package(package_info):
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
    command = commands.get(payload[2], None)

    if (not command) or (int(payload[0]) > int(payload[1])):
        print_action_result(ERROR, 'no command or package structure error')
        RF.sp_Send(ERROR, 'no command %s' % package_info['payload'])
        return 1

    command(RF, payload[3:])


def beacon():
    RF.sp_Send(DATA, '1;1;beacom')
    print "Beacon sent"
    print "*----------------*"

if __name__ == "__main__":
    print "Initial protocol"
    RF = sp_kernel.SerialProtocol()

    sched = Scheduler()
    sched.start()
    sched.add_interval_job(beacon, seconds=10)

    print "Start monitoring"
    print "----------------"

    while True:
        if sp_kernel.ser.inWaiting():
            if RF.sp_packetAvailable:
                RF.sp_packetAvailable = False
            package_info = RF.sp_Read()

            if package_info:
                handle_package(package_info)
                print "monitoring ..."
