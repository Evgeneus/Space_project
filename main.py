#! /usr/bin/python
# coding: utf-8

import kernel.sp_kernel as sp_kernel
from helpers.visualizer import print_action_result

DATA = 'd'
COMMAND = 'c'
ERROR = 'r'
RECEIVE = 'v'


def func(a):
    print a

def response(package_info):
    if not package_info['package_type'] == COMMAND:
        print_action_result(ERROR, '%s not command' % package_info['package_type'])
        RF.sp_Send(ERROR, '%s not command' % package_info['package_type'])
        return 1

    command = commands.get(package_info['payload'], None)
    if not command:
        print_action_result(ERROR, 'no command %s' % package_info['payload'])
        RF.sp_Send(ERROR, 'no command %s' % package_info['payload'])
        return 1

    command(RF)

commands = {
    'a': func,
}

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
                response(package_info)
                print "monitoring ..."
