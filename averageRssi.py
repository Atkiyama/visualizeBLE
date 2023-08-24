import os
from node.packet import Packet
import re
import csv
import time as t
from node.device import Device
import sys


DEVICE_CSV = "device.csv"
addressDict = {}



# ログを読んで最もRSSIが大きいパケットを抽出する
def readLog(line,devices):
    
    mac_address_pattern = (r"([0-9A-Fa-f_]{2}[:-])([0-9A-Fa-f_]{2}[:-])([0-9A-Fa-f_]{2}[:-])([0-9A-Fa-f_]{2}[:-])([0-9A-Fa-f_]{2}[:-])([0-9A-Fa-f_]{2})")
    match_address = re.search(mac_address_pattern, line)
    address = match_address.group(1)+match_address.group(2)+match_address.group(3)+match_address.group(4)+match_address.group(5)+match_address.group(6) if match_address else None

    # 時刻の抽出
    time_regex = re.compile(r"(\d{2}:\d{2}:\d{2}\.\d{6})")
    match_time = re.search(time_regex, line)
    packet_time = match_time.group(1) if match_time else None

    #ManufactureCodeの抽出
    pattern = r"Manufacturer\(\d+\) = (\w+)"
    match = re.search(pattern, line)
    if match:
        manufacture = match.group(1)
    else:
        manufacture =None

    rssi_regex = re.compile(r"-?\d+ dBm")
    match_rssi = re.search(rssi_regex, line)
    rssi_origin = match_rssi.group() if match_rssi else None
    if rssi_origin:
        rssi = int(rssi_origin.split()[0])  # 数値部分のみを取得して整数に変換
    else:
        return
    if manufacture and address and packet_time and rssi:
        device = getDevice(devices,manufacture)
        if device.name == sys.argv[0]:
            if not address in addressDict:
                addressDict[address]=[]
            addressDict[address].append(Packet(packet_time,rssi,manufacture))
    
            
  

            
    if address and packet_time and rssi:
        #print(address+" "+time+" "+str(rssi)+" "+device.name)
        if not address in addressDict:
            addressDict[address]=[]
        addressDict[address].append(Packet(packet_time,rssi,manufacture))
    
    return address
        
        
# 最新のログファイルのパスを取得する
def getNewLog():
    log_folder = "log"
    files = os.listdir(log_folder)

    # ファイル名でソートして最新のログファイルを取得
    latest_log = max(files, key=lambda x: os.path.getctime(os.path.join(log_folder, x)))

    # パスを結合して最新のログファイルのパスを表示
    latest_log_path = os.path.join(log_folder, latest_log)

    return latest_log_path


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
        device = Device(d[1], d[0], d[2], d[3], d[4],d[5])
        devices[d[0]] = device  # uuidをキーとしてデバイスを辞書に追加
    return devices

def getDevice(devices,manufacture):
    for key in devices:
        if manufacture.startswith(key):
            return devices.get(key)
        
    return devices.get("None")

def getAverageRssi(address):
    packetList=addressDict[address]
    sum=0
    for packet in packetList:
        sum = sum + packet.rssi
    return sum/100


def main():
    # ここを新規ファイルが現れたら実行にする
    devices = getDeviceList(DEVICE_CSV)
    
    for line in sys.stdin:

       

        #print(line)

        # 行をスペースで区切って3つの値として読み込む
        try:
            address=readLog(line,devices)
            if address in addressDict:
                print(address+" "+type(addressDict[address]))
            if len(addressDict[address])==100:
                print("実験が終了しました")
                print("address:"+address+",平均RSSI="+getAverageRssi(address))
        except ValueError as e:
            print("Invalid input format. Skipping this line.",e)
            print(line)
            #print(" time ="+time +" rssi = "+rssi+" manufacture = "+ manufacture)
            continue
        except AttributeError as e:
            print("AttributeError occurred:", e)
            print(line)
            #print(" time ="+time +" rssi = "+rssi+" manufacture = "+ manufacture)
            continue



if __name__ == "__main__":
    main()
