'''
要求：1.发送请求
2.合理解析提取数据
3.保存至表格
'''

import requests
import json
import csv
import pandas as pd
import os


# 确定请求头、网址和请求方式
url = "https://www.bkchina.cn/product/productList"#注意网址的选取，要找找自己的数据在哪里
h = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
}
D = {
    "type":"ham"
}
response = requests.post(url,data=D,headers = h)
# print(response)



# 数据解析、提取
result = json.loads(response.text)
# print(result)
series = ["国王臻选","经典系列","超值系列"]
datas = []
# print(series1_datas)
def find (series):
    source = result[series]
    for i in source :
        data = {
            "中文名": i["FName"],
            "英文名": i["FNameEng"],
            "图片地址": i["FPicMiniUrl"]
        }
        datas.append(data)

for i in series:
    find(i)

# print(datas)


# 数据保存
if not os.path.exists("03数据"):
    os.makedirs("03数据")

datas1 = pd.DataFrame(datas)
datas1.to_excel("03数据/汉堡王excel表格数据.xlsx",index=False)

keys = datas[0].keys()
with open ("03数据/汉堡王CSV数据","w") as f:
    datas2 = csv.DictWriter(f,keys)
    datas2.writeheader()
    datas2.writerows(datas)


