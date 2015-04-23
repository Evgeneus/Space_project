#! /usr/bin/python
# coding: utf-8

import kernel.sp_kernel as sp_kernel
from helpers.visualizer import print_action_result


def response(package_info):
    if not package_info['package_type'] == 'c':
        print_action_result('r', 'not command')
        RF.sp_Send("error")


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
