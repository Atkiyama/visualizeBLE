import datetime
import random

now = datetime.datetime.now()
formatted_time = now.strftime("%H:%M:%S.%f")

while True:
    now = datetime.datetime.now()
    formatted_time = now.strftime("%H:%M:%S.%f")
    
    # ランダムなRSSIの値を生成
    rssi = random.randint(-99, -11)
    
    # データを組み立てて表示
    data = f"{formatted_time} 52:43:a6:30:4a:12 (random) [0] {rssi} dBm Complete 16b Services(3) = 00001111-0000-1000-8000-00805f9b34fb"
    print(data)
