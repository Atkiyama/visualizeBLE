import os
from datetime import datetime
from node.packet import Packet
import re

DEVICE_CSV = "device.csv"
MIN_RSSI=-80



# ログを読んで最もRSSIが大きいパケットを抽出する
def readLog(path):
    max_rssi = -10000
    # 現在時刻を取得
    current_time = datetime.now()

    # 指定された形式で時刻を文字列に変換
    time_string = current_time.strftime("%H:%M:%S.%f")[:-3]
    packet = Packet(time_string, max_rssi,None)
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            

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

            if time and rssi and int(rssi) > max_rssi and int(rssi) > int(MIN_RSSI):
                max_rssi = int(rssi)
                packet = Packet(time, rssi, manufacture)

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




def main():
    # ここを新規ファイルが現れたら実行にする

    before = ""
    while True:
        latest = getNewLog()
        if latest != before:
            try:
                packet = readLog(latest)
                if packet  != None:
                    print(packet.time, packet.rssi, packet.manufacture,flush=True)
                else:
                    print("パケットを検出できませんでした")
            except FileNotFoundError:
                pass
        before = latest


if __name__ == "__main__":
    main()
