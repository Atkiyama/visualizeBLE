import re

# 与えられたログ
log = "Manufacturer(255) = 4c000215010e200b998f010009361336d71524ce83bbdcc6aec4429394"
# 正規表現パターンを定義
pattern = r"Manufacturer\(\d+\) = (\w+)"

# 正規表現にマッチする部分を検索
match = re.search(pattern, log)

# マッチした場合は"manufacture"の値を取得し、表示する
if match:
    manufacture_value = match.group(1)
    print("manufacture:", manufacture_value)
else:
    print("manufacture not found in the log.")
