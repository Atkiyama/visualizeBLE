

import sys
import csv
import time
import math
from node.device import Device

DEVICE_CSV="device.csv"
#機器の情報を読み込む
#現状未使用
def readCSV(path):
    data = []
    with open(path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダー行をスキップ
        for row in reader:
            data.append(row)
    return data

#デバイスのリストの取得
#現在未使用
def getDeviceList(path):
    data = readCSV(path)
    devices = {}
    for d in data:
        device = Device(d[1], d[0], d[2], d[3], d[4])
        devices[d[0]] = device  # uuidをキーとしてデバイスを辞書に追加
    return devices

def getDevice(devices,manufacture):
    for key in devices:
        if manufacture.startswith(key):
            return devices.get(key)
        
    return devices.get("none")
def main():
    # Neoクラスのインスタンスを作成
   
    devices = getDeviceList(DEVICE_CSV)
    
    from_to = True
    for line in sys.stdin:
        # 行をスペースで区切って3つの値として読み込む
        try:
            time, rssi, manufacture = line.strip().split()
            device = getDevice(devices,manufacture)
            print("show packet")
            print("name = "+device.name+" time ="+time +" rssi = "+rssi+" manufacture = "+ manufacture)
            print("color R:"+str(device.R)+" G:"+str(device.G)+" B:"+str(device.B))
           
        except ValueError:
            print("Invalid input format. Skipping this line.")
            continue

if __name__ == "__main__":
    main()