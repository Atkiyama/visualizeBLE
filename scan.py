from bluepy.btle import Scanner, DefaultDelegate
import bluepy.btle as btle
import datetime
import visualize
import capture
import frames
import tkinter.messagebox as MSG
import heapq
from dotenv import load_dotenv
from packet import Packet  # 外部モジュールからPacketクラスをインポート
from device import Device
from csv_reader import read

load_dotenv()

# 環境変数を参照
import os
LOWER_RSSI = int(os.getenv("LOWER_RSSI"))
CAPTURE_TIME = float(os.getenv("CAPTURE_TIME"))
DEVICE_CSV_PATH=os.getenv("DEVICE_CSV_PATH")
neo = visualize.Neo()
from_to = True
dict_frame = frames.Dictionary.dicts

deviceCSV=read(DEVICE_CSV_PATH)
#デバイスの辞書
device_dict = {}

for d in deviceCSV:
    device_dict[d.uuid] = Device(d.uuid, d.name, d.R, d.G, d.B)
   
packet_heap = []

class ScanDelegate(DefaultDelegate):
    def __init__(self):
         DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
         t_now = datetime.datetime.now().time()
        
            
         if (dev.rssi > LOWER_RSSI):
               #if dev.addr == air:
            print("%s %s (%s) [%s] %s dBm" % (t_now, dev.addr, dev.addrType, dev.iface, dev.rssi))
            uuid=None
            for (adtype, desc, value) in dev.getScanData():
                if desc == 'Complete 16b Services' and adtype == 3:
                    uuid = value[4:8]  # UUIDを取得
                    print("UUID:", uuid)
               
            print("")
            
            #LEDを光らせるメソッドの呼び出し
            print("%s dBm" % (dev.rssi))
            if(uuid):   
               packet = Packet(t_now, dev.rssi, uuid)
               heapq.heappush(packet_heap, (packet.rssi, packet))
               print("pushed")
               print()

def get_packet_from_heap():
    if packet_heap:
        _, packet = heapq.heappop(packet_heap)
        return packet
    else:
        return None

scanner = Scanner().withDelegate(ScanDelegate())
while True:
       try:
               scanner.scan(CAPTURE_TIME)
               packet=get_packet_from_heap()
               packet_heap = []
               device=device_dict(packet.uuid)
               neo.light(from_to, device)
       except btle.BTLEException:
           print('BTLE Exception while scanning')
               #MSG('BTLE Exception while scanning')
