from bluepy import btle

class MyDelegate(btle.DefaultDelegate):
    def __init__(self) :
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self,cHandle,data):
        print("handling notification...")
#        print(cHandle) #18
        print(data)
        dev.writeCharacteristic(cHandle, 'y')

print "Connecting..."

dev = btle.Peripheral("90:E2:02:9F:DA:75")

print "Services..."

dev.withDelegate(MyDelegate())

#for dsc in dev.getDescriptors() :
#       print(dsc)
#       print(" {}".format(dsc.uuid))

## send data to Uno
#svc = dev.getServiceByUUID("ffe0")

#for ch in svc.getCharacteristics() :
#       print(ch.propertiesToString())
#       print(ch.getHandle()) #18

#ch = svc.getCharacteristics()[0]
#ch.write('\n')
#ch.write( 'n' )
#ch.write('\n')

dev.writeCharacteristic(18, '\nconnected\n')

while True:
        if dev.waitForNotifications(1.0):
                continue
        print("waiting...")

dev.disconnect()
