#! /usr/bin/python
# coding: utf-8

import kernel.sp_kernel as sp_kernel
from kernel.commands import commands
from helpers.visualizer import print_action_result

DATA = 'd'
COMMAND = 'c'
ERROR = 'r'
RECEIVE = 'v'


def handle_command(package_info):
    if not package_info['package_type'] == COMMAND:
        print_action_result(ERROR, '%s not command' % package_info['package_type'])
        RF.sp_Send(ERROR, '%s not command' % package_info['package_type'])
        return 1

    command = commands.get(package_info['payload'].split(';')[2], None)
    if not command:
        print_action_result(ERROR, 'no command %s' % package_info['payload'])
        RF.sp_Send(ERROR, 'no command %s' % package_info['payload'])
        return 1

    command(RF, package_info['payload'])


if __name__ == "__main__":
    print "Initial protocol"
    RF = sp_kernel.SerialProtocol()

    print "Start monitoring"
    print "----------------"

    while True:
        if sp_kernel.ser.inWaiting():
            if RF.sp_packetAvailable:
                RF.sp_packetAvailable = False
            package_info = RF.sp_Read()

            if package_info:
                handle_command(package_info)
                print "monitoring ..."

    # RF.sp_Send('c', 'a')
