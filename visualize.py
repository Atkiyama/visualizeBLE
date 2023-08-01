from typing import OrderedDict
import board
import neopixel
import sys
import csv
import time
import math
from node.device import Device


DEVICE_CSV="device.csv"



class Neo:
    # シリアルLEDの初期化
    ##ピンの情報
    pixel_pin = board.D18
    #ピクセル数
    num_pixels = 16*16
    #LEDストリップのカラーチャネルの順序（ここでは青、緑、赤）
    ORDER = neopixel.GRB
    # brightnessをあげると光が強くなるが、上げすぎると白になる
    # auto_writeをtrueにするとpixels[]にアクセスした時点でLEDが点灯消灯する
    pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=0.010, auto_write=False, pixel_order=ORDER
    )
    #テスト用
    n = 0

    """"
    __init__と合わせて
    neopixelで扱う添え字を扱いやすいようにする
    [1,2,3]    [1,2,3]
    [6,5,4] to [4,5,6]
    [7,8,9]    [7,8,9]
    """
    
    #秋山メモ
    #実際は左のような配列が生成される
    list_linking = []
    for i in range(0, 16):
        sublist = []
        for j in range(0, 16):
            if int((i*16+j)/16)%2 == 0:
                sublist.append(i*16+j)
            else:
                sublist.append((i+1)*16-j-1)
        list_linking.append(sublist)

    def __init__(self) -> None:
        #基準点
        self.small_standard = 7
        self.big_standard = 8
        #光らせる座標のリスト
        self.list_coordiante = []
        for i in range(0, 8):
            sublist = self.substitution()
            self.list_coordiante.append(sublist)
            self.small_standard -= 1
            self.big_standard += 1

    #同時に光らせる座標の設定
    def substitution(self):
        list_return = []
        for j in range(0, self.big_standard-self.small_standard+1):
            list = [self.small_standard, self.small_standard+j]
            list_return.append(list)
        
        for j in range(0, self.big_standard-self.small_standard+1):
            list = [self.small_standard+j, self.small_standard]
            if not(list in list_return):
                list_return.append(list)
        
        for j in range(0, self.big_standard-self.small_standard+1):
            list = [self.small_standard+j, self.big_standard]
            if not(list in list_return):
                list_return.append(list)

        for j in range(0, self.big_standard-self.small_standard+1):
            list = [self.big_standard, self.small_standard+j]
            if not(list in list_return):
                list_return.append(list)

        return list_return

    # 消灯
    def turn_off(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    # 順番に表示
    def order(self):
        for i in range(256):
            i = self.arrangePosition(i)
            self.pixels[i] = (0, 0, 255)
            self.pixels.show()
            time.sleep(0.1)
            self.pixels[i] = (0, 0, 0)
            self.pixels.show()

    # 制御しやすい位置番号の設定
    # 16で割ったとき、偶数の時は何もしないが、奇数の時はその行での値を入れ替える
    #使ってない
    def arrangePosition(x):
        if math.floor(x/16 % 2) == 1:
            int_list = [math.floor(x/16)*16+i for i in range(16)]
            int_list.reverse()
            return int(int_list[x % 16])
        else:
            return x

    # フレームキャプチャ時の光らせるメソッド
    # from_to はTrueの時内から外、Falseの時外から内
    def light(self, from_to, device):
        #print(device.uuid,device.name,device.R, device.G, device.B)
        # 内から外の時
        fr = 0
        to = 8
        updown = 1
        # 外から内の時
        if from_to == False:
            fr = 7
            to = -1
            updown = -1
        for i in range(fr, to, updown):
            for j in range(0, len(self.list_coordiante[i])):
                # 座標の取得
                a = self.list_coordiante[i][j][0]
                b = self.list_coordiante[i][j][1]
                # 光らせる位置の決定
                c = self.list_linking[a][b]
                # 座標に rgb 設定
                self.pixels[c] = (device.R, device.G, device.B)
            self.pixels.show()
            # この時間で光る速度を変更できる
            time.sleep(0.02)
            self.turn_off()

    #テスト用の光らせるメソッド
    def direct_test(self, device):
        self.pixels[self.n] = (device.R, device.G, device.B)
        self.pixels.show()
        self.n += 1

#機器の情報を読み込む
#現状未使用
def readCSV(path):
    data = []
    with open(path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダー行をスキップ
        for row in reader:
            data.append(row)
    return data

#デバイスのリストの取得
#現在未使用
def getDeviceList(path):
    data = readCSV(path)
    devices = {}
    for d in data:
        device = Device(d[1], d[0], d[2], d[3], d[4])
        devices[d[0]] = device  # uuidをキーとしてデバイスを辞書に追加
    return devices

def getDevice(devices,manufacture):
    for key in devices:
        if manufacture.startswith(key):
            return devices.get(key)
        
    return devices.get("none")

def main():
    devices = getDeviceList(DEVICE_CSV)
    neo = Neo()
    from_to = True
    for line in sys.stdin:
        # 行をスペースで区切って3つの値として読み込む
        try:
            time, rssi, manufacture = line.strip().split()
            device = getDevice(devices,manufacture)
            print("show packet")
            if device.name and rssi and device.manufacture:
                print("name = "+device.name+" time ="+time +" rssi = "+rssi+" manufacture = "+ manufacture)
                print("color R:"+str(device.R)+" G:"+str(device.G)+" B:"+str(device.B))
                neo.light(from_to, device)
            else:
                 print("None packet")
                 continue
        except ValueError:
            print("Invalid input format. Skipping this line.")
            continue
        except AttributeError as e:
            print("AttributeError occurred:", e)
            continue

        
        
if __name__ == "__main__":
    main()