import sp_kernel

print "Initial protocol"
RF = sp_kernel.SerialProtocol()

print "Start monitoring"
print "----------------"

while True:
    if sp_kernel.ser.inWaiting():
        if RF.sp_packetAvailable:
            RF.sp_packetAvailable = False
        data = RF.sp_Read()
