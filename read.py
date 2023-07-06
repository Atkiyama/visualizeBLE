import csv


def read(path):
    data = []
    with open(path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダー行をスキップ
        for row in reader:
            data.append(row)
    return data
