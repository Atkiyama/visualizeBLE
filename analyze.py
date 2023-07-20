import csv
import os
from node.device import Device
from node.packet import Packet
import re

DEVICE_CSV = "device.csv"

# 機器の情報を読み込む
# 現状未使用
def readCSV(path):
    data = []
    with open(path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダー行をスキップ
        for row in reader:
            data.append(row)
    return data

# ログを読んで最もRSSIが大きいパケットを抽出する
def readLog(path):
    max_rssi = -10000
    packet = None
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            

            # 時刻の抽出
            time_regex = re.compile(r"(\d{2}:\d{2}:\d{2}\.\d{6})")
            match_time = re.search(time_regex, line)
            time = match_time.group(1) if match_time else None

            # UUIDの抽出
            uuid_regex = uuid_regex = re.compile(r"(?i)\bComplete 16b Services\b.*\b([0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12})\b")
            match_uuid = re.search(uuid_regex, line)
            uuid = match_uuid.group(1) if match_uuid else None

            # RSSIの抽出
            rssi_regex = re.compile(r"-?\d+ dBm")
            match_rssi = re.search(rssi_regex, line)
            rssi = match_rssi.group() if match_rssi else None

            # Noneでないことを確認してからスライスする
            if rssi != None:
                rssi = rssi[0:3]
            else:
                continue

            if time and uuid and rssi and int(rssi) > max_rssi:
                max_rssi = int(rssi)
                packet = Packet(time, rssi, uuid[4:8])

    return packet

# 最新のログファイルのパスを取得する
def getNewLog():
    log_folder = "log"
    files = os.listdir(log_folder)

    # ファイル名でソートして最新のログファイルを取得
    latest_log = max(files, key=lambda x: os.path.getctime(os.path.join(log_folder, x)))

    # パスを結合して最新のログファイルのパスを表示
    latest_log_path = os.path.join(log_folder, latest_log)

    return latest_log_path

# デバイスのリストの取得
# 現在未使用
def getDeviceList(path):
    data = readCSV(path)
    devices = []
    for d in data:
        device = Device(d[1], d[0], d[2], d[3], d[4])
        devices.append(device)
    return devices


def main():
    # ここを新規ファイルが現れたら実行にする

    before = ""
    while True:
        latest = getNewLog()
        if latest != before:
            try:
                packet = readLog(latest)
                if packet  != None:
                    print(packet.time, packet.rssi, packet.uuid,flush=True)
                else:
                    print("UUIDを含むパケットを検出できませんでした")
            except FileNotFoundError:
                pass
        before = latest


if __name__ == "__main__":
    main()
