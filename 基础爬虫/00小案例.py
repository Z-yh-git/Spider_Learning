"""
爬取图片
"""

# import requests
# import os
# url = "https://image.baidu.com/search/detail?adpicid=0&b_applid=7375285026672944883&bdtype=0&commodity=&copyright=&cs=3829395457%2C4172406290&di=7565560840087142401&fr=click-pic&fromurl=http%253A%252F%252Fweibo.com%252F7395465900%252FOz6Ej1tPL&gsm=1e&hd=&height=0&hot=&ic=&ie=utf-8&imgformat=&imgratio=&imgspn=0&is=0%2C0&isImgSet=&latest=&lid=96c433bb006a5614&lm=&objurl=https%253A%252F%252Fww4.sinaimg.cn%252Fmw690%252F0084uCw4gy1hu3olfucisj31tw3y8b29.jpg&os=4069894074%2C1381679135&pd=image_content&pi=0&pn=23&rn=1&simid=4245432502%2C671869493&tn=baiduimagedetail&width=0&word=%E6%A2%85%E8%A5%BF&z="
# h = {
#     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
#
# }
#
# img = requests.get(url = url,headers=h)
# # print(img)<Response [200]>
#
# # if not os.path.exists("00数据"):
# #     os.mkdir("00数据")
#
# with open("messi.png","wb") as f:
#     f.write(img.content)
# print("运行成功")
#


'''
demo = {
    "name":"哪吒",
    "age":1000,
    "thing":"脑海"
}
将此数据转化为Json格式存储
追加写入"\n努力不一定成功，但不努力一定很轻松"
\n只是强制换行
'''

# demo = {
#     "name":"哪吒",
#     "age":1000,
#     "thing":"脑海"
# }
# import json
# with open("00数据/魔丸.json","w",encoding="utf-8") as f:
#     json.dump(demo,f,ensure_ascii=False)
# with open("00数据/魔丸.json","a",encoding="utf-8") as A:
#     A.write("\n努力不一定成功，但不努力一定很轻松")




'''
数据读取
利用已经爬下来的数据练习读取操作，要求包括excel、CSV和文本数据
'''


# import pandas as pd
# import csv
# data1 = pd.read_excel("01数据/bookdata.xlsx")
# # print(data1)
# with open("01数据/豆瓣图书CSV数据.csv","r") as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print(row)#注意：需要用遍历才可以访问到具体的所有数据



"""
从文本中提取航班号、出发地、目的地和起飞时间
text4 = '''
CA1853 北京-上海 08:30
MU2501 广州-成都 14:15
CZ3107 深圳-北京 19:40
HU7632 上海-西安 07:55
'''
"""

text4 = '''
CA1853 北京-上海 08:30
MU2501 广州-成都 14:15
CZ3107 深圳-北京 19:40
HU7632 上海-西安 07:55
'''

import re
rule = r'([A-Z]{2}\d{4}).+?(\w{2}-\w{2}).+?(.+)'
result = re.findall(rule, text4)
print(result)
