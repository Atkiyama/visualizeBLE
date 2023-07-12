import re

data = "14:53:48.056859 52:43:a6:30:4a:12 (random) [0] -71 dBm Complete 16b Services(3) = 00001111-0000-1000-8000-00805f9b34fb"

# 時刻の抽出
time_regex = re.compile(r"(\d{2}:\d{2}:\d{2}\.\d{6})")
match_time = re.search(time_regex, data)
time = match_time.group(1) if match_time else None

# UUIDの抽出
uuid_regex = re.compile(r"= ([0-9a-fA-F-]+)$")
match_uuid = re.search(uuid_regex, data)
uuid = match_uuid.group(1) if match_uuid else None

# RSSIの抽出
rssi_regex = re.compile(r"-?\d+ dBm")
match_rssi = re.search(rssi_regex, data)
rssi = match_rssi.group() if match_rssi else None

# 結果の出力
print("時刻:", time)
print("UUID:", uuid)
print("RSSI:", rssi)
