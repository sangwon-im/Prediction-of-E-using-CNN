import json
import os

sum = 0

for i in range(1, 6000):
    try:
        with open(f"raw/etc/{i}_data.json", "r") as f:
            data = json.load(f)
        sum += float(data['Calculation time'])
    except FileNotFoundError as e:
        print(e)

print(sum/6000)