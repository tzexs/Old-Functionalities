import json
import pandas as pd

with open("path/file.json", encoding=' utf-8') as my_json:
    data = json.load(my_json)

print(data)
df = pd.DataFrame(data)
df.to_excel("data.xlsx",index = None, header = False, encoding = 'utf-8')