#仮想的にパケットキャプチャのデータを出力するコード
import datetime
import random

now = datetime.datetime.now()
formatted_time = now.strftime("%H:%M:%S.%f")

while True:
    now = datetime.datetime.now()
    formatted_time = now.strftime("%H:%M:%S.%f")
    
    # ランダムなRSSIの値を生成
    rssi = random.randint(-99, -11)
    #Manufacturer(255) = 4c0012010e200b998f010009361336d71524ce83bbdcc6aec4429394"
    # データを組み立てて表示
    #52:43:a6:30:4a:12
    data = f"52:43:a6:30:4a:12 (random) [0] {rssi} dBm Manufacturer(255) = 4c0012010e200b998f010009361336d71524ce83bbdcc6aec4429394"
    print(data)
