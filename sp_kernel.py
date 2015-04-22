#! /usr/bin/python
# coding: utf-8

import serial

serial_name = "/dev/ttyUSB0"
read_byte_mode = 1

ser = serial.Serial(serial_name,  19200, timeout=1)
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
        self.sp_dataString = " "
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
                if self.sp_dataLength <= 0:
                    self.sp_dataLength = ord(bufferChar)
                    print 'data length: %s' % self.sp_dataLength

                else:
                    if self.sp_dataLength >= len(self.sp_dataString):
                        self.sp_dataString += str(bufferChar)
                    else:
                        if self.sp_stopMarkerStatus < len(self.sp_stopMarker):
                            if self.sp_stopMarker[self.sp_stopMarkerStatus] == bufferChar:
                                self.sp_stopMarkerStatus += 1
                                if self.sp_stopMarkerStatus == len(self.sp_stopMarker):
                                    print 'data: %s' % self.sp_dataString
                                    self.sp_Reset()
                                    self.sp_packetAvailable = True
                                    print "Packet is received"
                                    print "*----------------*"
                                    print "monitoring ..."

                                    return self.sp_dataString
                            else:
                                print "Packet don't received"
                                print "*----------------*"
                                print "monitoring ..."

                                self.sp_ResetAll()
    def sp_Send(self, data):
        package = " " + self.sp_startMarker + chr(int(len(data))) + data + self.sp_stopMarker + " "
        ser.write(package)

        print "Package send:"
        print package