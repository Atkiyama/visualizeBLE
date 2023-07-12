from collections import defaultdict
from math import trunc

class Dictionary:
    dict = defaultdict(list)
    # 0:フレーム名, 1:R, 2:G, 3:B, 4:表示するか, 5:取得回数
    dict = {'8':['beacon', 0, 0, 255, False, 0], #青
            '4':['request probe', 0, 255, 0, False, 0], #ライム
            '5':['response probe', 255, 255, 0, False, 0], #黄色
            '0':['request associate', 255, 255, 255, False, 0], #白 
            '1':['response associate', 0, 255, 255, False, 0], #アクア
            '11':['authentication', 0, 128, 0, False, 0], #緑
            '12':['deauthentication', 255, 0, 255, False, 0], #ピンク
            '10':['reject authentication', 255, 165, 0, False, 0], #オレンジ
            '27':['RTS', 127, 255, 212, False, 0], #アクアマリン
            '28':['CTS', 255, 255, 224, False, 0], #ライトイエロー
            '29':['ACK', 255, 0, 0, False, 0], #赤
            '32':['data', 128, 0, 128, False, 0], #紫
            '36':['null data', 128, 0, 128, False, 0], #紫
    }

    # ビーコンを表示
    def beacon(self):
        self.changeTrue('8')

    #プローブ要求、応答を表示
    def probe(self):
        self.changeTrue('4')
        self.changeTrue('5')

    #アソシエーション要求、応答、拒否を表示
    def associate(self):
        self.changeTrue('0')
        self.changeTrue('1')
        self.changeTrue('10')

    #認証、非認証を表示
    def authentication(self):
        self.changeTrue('11')
        self.changeTrue('12')
    
    # RTS/CTSを表示
    def rtscts(self):
        self.changeTrue('27')
        self.changeTrue('28')
    
    # ACKを表示
    def ack(self):
        self.changeTrue('29')
    
    # データフレームを表示
    def data(self):
        self.changeTrue('32')
        self.changeTrue('36')

    #dict[4]をTrueに
    def changeTrue(self, n):
        self.dict[n][4] = True
    
    #dict[4]をFalseに
    def changeFalse(self, n):
        self.dict[n][4] = False

    #カウントアップ
    def countUp(self, frame):
        self.dict[frame][5] += 1

    #取得回数の表示
    def printCount(self, router, device):
        num = 0
        print(' ')
        print('---end---')
        print()
        for mykey in self.dict.keys():
            num += self.dict[mykey][5]
            line = self.dict[mykey][0] + ' : ' + str(self.dict[mykey][5])
            print(line)
        line_total = 'total : ' + str(num)
        print(line_total)
        print()
        print(f'router:{router} device:{device}')
        print()

""""
    def main(self):
        val = self.dict
        print(val['8'])
        val['8'][4] = True
        print(val['8'])
    
if __name__ == "__main__":
    a = Dictionary()
    a.main()

"""