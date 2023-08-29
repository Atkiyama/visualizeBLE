import pandas as pd
import matplotlib.pyplot as plt

# CSVファイルを読み込む
csv_file = '予備実験.csv'
df = pd.read_csv(csv_file)

# グラフを作成して表示する
plt.figure(figsize=(10, 6))

# カラム名に合わせて修正
plt.plot(df.iloc[:, 0], df['FindMy'], marker='o', label='FindMy')
plt.plot(df.iloc[:, 0], df['Airtag'], marker='o', label='Airtag')
plt.plot(df.iloc[:, 0], df['iBeacon'], marker='o', label='iBeacon')

plt.xlabel('Distance')
plt.ylabel('Signal Strength')
plt.title('Signal Strength Comparison')
plt.legend()

plt.grid(True)
plt.show()
