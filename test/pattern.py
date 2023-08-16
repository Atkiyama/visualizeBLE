import re

# テキストファイルの内容を読み込む
with open('log/1803.txt', 'r') as file:
    text = file.read()

# Macアドレスを抽出する正規表現パターン
mac_address_pattern = r'([0-9A-Fa-f_]{2}[:-])([0-9A-Fa-f_]{2}[:-])([0-9A-Fa-f_]{2}[:-])([0-9A-Fa-f_]{2}[:-])([0-9A-Fa-f_]{2}[:-])([0-9A-Fa-f_]{2})'

# 正規表現でマッチする部分を全て抽出する
mac_addresses = re.findall(mac_address_pattern, text)

# マッチしたMacアドレスを表示する
for mac_address in mac_addresses:
    print(mac_address)
