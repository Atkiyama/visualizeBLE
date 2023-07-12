import csv
import os
from device import Device
from packet import Packet
import re

DEVICE_CSV="device.scv"

#機器の情報を読み込む
def readCSV(path):
    data = []
    with open(path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダー行をスキップ
        for row in reader:
            data.append(row)
    return data

def readLog(path):
    # ファイルを開いて一行ずつ読み込む
    packets = []
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
        # 時刻の抽出
        time_regex = re.compile(r"(\d{2}:\d{2}:\d{2}\.\d{6})")
        match_time = re.search(time_regex, line)
        time = match_time.group(1) if match_time else None

        # UUIDの抽出
        uuid_regex = re.compile(r"= ([0-9a-fA-F-]+)$")
        match_uuid = re.search(uuid_regex, line)
        uuid = match_uuid.group(1) if match_uuid else None

        # RSSIの抽出
        rssi_regex = re.compile(r"-?\d+ dBm")
        match_rssi = re.search(rssi_regex, line)
        rssi = match_rssi.group() if match_rssi else None
    
        packet = Packet(time,rssi,uuid[4:8])
        packets.append(packet)
    return packet

def getNewLog():
    files = os.listdir("log")

    # ファイル名でソートして最新のログファイルを取得
    latest_log = max(files, key=os.path.getctime)

    # 最新のログファイルのパスを表示
    latest_log_path = os.path.join("log", latest_log)
    return latest_log_path

def getDeviceList(path):
    data=readCSV(path)
    devices = []
    for d in data:
        device = Device(d.name,d.uuid,d.R,d.G,d.B)
        devices.append(device)
    return devices

def getMaxPacket(packets):
    max = packets[0]
    for packet in packets:
        if max.rssi < packet.rssi:
            max = packet
    
    return max

        
    
def main():
    devices = getDeviceList(DEVICE_CSV)
    while True:
        latest_new_log = getNewLog()
        packets = readLog(latest_new_log)
        packet = getMaxPacket(packets)
        print(packet.time+" "+packet.rssi+" "+ packet.uuid)
        
    
    
    
if __name__ == "__main__":
    main()
