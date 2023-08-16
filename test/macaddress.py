import re
from collections import defaultdict
import statistics

# テキストファイルからデータを読み取る関数
def read_log_data(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# MACアドレスごとのRSSIを格納する辞書を作成
mac_rssi_dict = defaultdict(list)

# テキストファイルからデータを読み取る（適切なファイルパスを指定してください）
file_path = 'output.txt'
log_data = read_log_data(file_path)

# 行ごとにログを処理し、MACアドレスとRSSIを抽出して辞書に格納
pattern = r"([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}"  # MACアドレスを抽出するための正規表現パターン
for line in log_data.splitlines():
    mac_match = re.search(pattern, line)
    if mac_match:
        mac_address = mac_match.group(0).lower()
        rssi = None
        for part in reversed(line.split()):
            if part.startswith("-"):
                try:
                    rssi = int(part)
                    break
                except ValueError:
                    continue
        if rssi is not None:
            mac_rssi_dict[mac_address].append(rssi)

# ユニークなMACアドレスごとに平均値、標準偏差、パケット数を計算して表示
for mac_address, rssi_list in mac_rssi_dict.items():
    avg_rssi = statistics.mean(rssi_list)
    std_dev_rssi = statistics.stdev(rssi_list) if len(rssi_list) > 1 else 0
    packet_count = len(rssi_list)
    print(f"MACアドレス: {mac_address}, 平均RSSI: {avg_rssi:.2f} dBm, 標準偏差: {std_dev_rssi:.2f} dBm, パケット数: {packet_count}")
