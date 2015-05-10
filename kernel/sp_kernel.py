#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time

serial_name = "/dev/ttyS0"
read_byte_mode = 1

ser = serial.Serial(serial_name,  19200, timeout=1.3)
print "Serial port name:"
print ser.name


class SerialProtocol():
    def __init__(self):
        self.sp_startMarker = "<strm>"
        self.sp_stopMarker = "<stpm>"
        self.sp_packetAvailable = False
        self.sp_startMarkerStatus = 0
        self.sp_stopMarkerStatus = 0
        self.sp_dataLength = 0
        self.sp_dataString = ""
        self.sp_package_type = ""
        # ser.write("+++")
        # time.sleep(1)
        # ser.write("AT+IPR=19200\r")
        # time.sleep(1)
        # ser.write("ATO\r")
        # time.sleep(1)
        print ser.readall()

    def sp_Reset(self):
        self.sp_startMarkerStatus = 0
        self.sp_stopMarkerStatus = 0
        self.sp_dataLength = 0
        self.sp_packetAvailable = False
        self.sp_package_type = ""

    def sp_ResetAll(self):
        self.sp_dataString = " "
        self.sp_Reset()

    def sp_Read(self):
        if not self.sp_packetAvailable:
            bufferChar = ser.read(read_byte_mode)
            if ( self.sp_startMarkerStatus < len(self.sp_startMarker) ):
                if ( self.sp_startMarker[self.sp_startMarkerStatus] == bufferChar ):
                    self.sp_startMarkerStatus += 1
                else:
                    self.sp_ResetAll()
            else:
                if not self.sp_package_type:
                    self.sp_package_type = str(bufferChar)
                    return

                if self.sp_dataLength <= 0:
                    self.sp_dataLength = ord(bufferChar)
                    print 'data length: %s' % self.sp_dataLength
                    return

                else:
                    if self.sp_dataLength >= len(self.sp_dataString):
                        self.sp_dataString += str(bufferChar)
                    else:
                        if self.sp_stopMarkerStatus < len(self.sp_stopMarker):
                            if self.sp_stopMarker[self.sp_stopMarkerStatus] == bufferChar:
                                self.sp_stopMarkerStatus += 1
                                if self.sp_stopMarkerStatus == len(self.sp_stopMarker):
                                    print 'data: %s' % self.sp_dataString
                                    print "Package is received"
                                    print "*----------------*"

                                    package_info = {'package_type': self.sp_package_type, 'payload': self.sp_dataString.strip()}

                                    self.sp_Reset()
                                    self.sp_packetAvailable = True

                                    return package_info
                            else:
                                print "Package don't received"
                                print "*----------------*"
                                print "monitoring ..."

                                self.sp_ResetAll()

    def sp_Send(self, package_type, data):
        package = " " + self.sp_startMarker + package_type + chr(int(len(data))) + data + self.sp_stopMarker + " "
        ser.write(package)

        print "Package send: "
        print "Data: %s" % data
        print "Package: %s" % package
        print "*----------------*"

        time.sleep(0.5)