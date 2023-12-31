from typing import OrderedDict
import board
import neopixel
import time
import math
#import numpy


class Neo:
    # シリアルLEDの初期化
    pixel_pin = board.D18
    num_pixels = 16*16
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
        #
        #二次元配列になっていてi番目に光らせる場所をj個用意する
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
    def light(self, from_to, detail_list):
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
                self.pixels[c] = (detail_list[1], detail_list[2], detail_list[3])
            self.pixels.show()
            # この時間で光る速度を変更できる
            time.sleep(0.02)
            self.turn_off()

    #テスト用の光らせるメソッド
    def direct_test(self, detail_list):
        self.pixels[self.n] = (detail_list[1], detail_list[2], detail_list[3])
        self.pixels.show()
        self.n += 1

    #def main(self):
        #self.turn_off()

        #li = [0, 0, 255, 0]
        
        #for i in range(0, 3):
            #self.light(True, li)
            
        #for i in range(0, 3):
            #self.light(False, li)

        #self.turn_off()


#if __name__ == "__main__":
    #ne = Neo()
    #ne.main()


