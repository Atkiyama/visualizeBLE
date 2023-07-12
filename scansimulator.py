import datetime


while True:
    now = datetime.datetime.now()
    formatted_time = now.strftime("%H:%M:%S.%f")
    time = formatted_time + " 52:43:a6:30:4a:12 (random) [0] -71 dBm Complete 16b Services(3) = 00001111-0000-1000-8000-00805f9b34fb"
    print(time);