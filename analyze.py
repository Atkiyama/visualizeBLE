import os
from datetime import datetime
from node.packet import Packet
import re
import csv
from node.device import Device


DEVICE_CSV = "device.csv"
MIN_RSSI=-40



# ログを読んで最もRSSIが大きいパケットを抽出する
def readLog(path,devices):
    max_rssi = -10000
    max_address =''
    max_manufacture =None
    # 現在時刻を取得
    current_time = datetime.now()

    # 指定された形式で時刻を文字列に変換
    time_string = current_time.strftime("%H:%M:%S.%f")[:-3]
    packet = Packet(time_string, max_rssi,None)
    addressDict = {}
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            
            
            # 正規表現パターンを定義
            mac_address_pattern = r"([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}"

            # ログからMACアドレスを抽出
            address = re.search(mac_address_pattern, line)

            # 時刻の抽出
            time_regex = re.compile(r"(\d{2}:\d{2}:\d{2}\.\d{6})")
            match_time = re.search(time_regex, line)
            time = match_time.group(1) if match_time else None

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

                # # Noneでないことを確認してからスライスする
                # if rssi != None:
                #     rssi = rssi[0:3]
            else:
                continue
            if manufacture:
                device = getDevice(devices,manufacture)
                rssi = rssi + device.vias

            if address and time and rssi and int(rssi) > max_rssi:
                if not address in addressDict:
                    addressDict[address]=[]
                addressDict[address].append(Packet(time,rssi,manufacture))
               
                
    for key in addressDict.keys():
        total=0
        tmp_manufacture=None
        for packet in addressDict[key]:
            total=total+packet.rssi
            if packet.manufacture:
                tmp_manufacture=packet.manufacture
        ave_rssi=total/len(addressDict[key])
        if max_rssi < ave_rssi:
            max_rssi = ave_rssi
            max_address = key
            max_manufacture=tmp_manufacture
            

    return Packet(addressDict[max_address][0].time,max_rssi,max_manufacture)

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


def main():
    # ここを新規ファイルが現れたら実行にする
    devices = getDeviceList(DEVICE_CSV)
    
    before = ""
    while True:
        latest = getNewLog()
        if latest != before:
            try:
                packet = readLog(latest,devices)
                if packet  != None:
                    print(packet.time, packet.rssi, packet.manufacture,flush=True)
                else:
                    print("パケットを検出できませんでした")
            except FileNotFoundError:
                pass
        before = latest


if __name__ == "__main__":
    main()
