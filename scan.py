from bluepy.btle import Scanner, DefaultDelegate
import bluepy.btle as btle
import datetime
import visualize
import capture
import frames
import tkinter.messagebox as MSG

class ScanDelegate(DefaultDelegate):
    def __init__(self):
               DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
               t_now = datetime.datetime.now().time()
               neo = visualize.Neo()
               dict_ins = frames.Dictionary()
               from_to = True
               frame = '0'
               dict_frame = frames.Dictionary.dict
               #使用したAirTagのMACアドレス
               air = "f5:8e:90:19:d7:2b"
               #使用したattagのMACアドレス
               att = "dc:1e:6c:e9:7c:48"
               #使用したiBeaconのMACアドレス
               ibe = "f7:71:03:e6:c5:15"
               #使用したMAMORIOのMACアドレス
               mam = "44:e4:ee:f6:20:99"
               if (dev.rssi > -80) and (dev.addr == air or dev.addr == att or dev.addr == ibe or dev.addr == mam):
               #if dev.addr == air:
                print("%s %s (%s) [%s] %s dBm" % (t_now, dev.addr, dev.addrType, dev.iface, dev.rssi))
                if dev.addr == air:
                   frame = '8'
                   print("AirTag")
                elif dev.addr == att:
                   frame = '29'
                   print("attag")
                elif dev.addr == ibe:
                   frame = '11'
                   print("iBeacon")
                elif dev.addr == mam:
                   frame = '5'
                   print("MAMORIO")
                for (adtype, desc, value) in dev.getScanData():
                   print(" %s(%s) = %s" % (desc, adtype, value))
                print("")
                #LEDを光らせるメソッドの呼び出し
                neo.light(from_to, dict_frame[frame])
                print("%s dBm" % (dev.rssi))
scanner = Scanner().withDelegate(ScanDelegate())
while True:
       try:
               scanner.scan(10.0)
               break
       except btle.BTLEException:
           print('BTLE Exception while scanning')
               #MSG('BTLE Exception while scanning')
