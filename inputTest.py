import sys


DEVICE_CSV="device.csv"





def main():
  
    for line in sys.stdin:
        # 行をスペースで区切って3つの値として読み込む
        print(line)
        #time, rssi, uuid = line.strip().split()
       
if __name__ == "__main__":
    main()