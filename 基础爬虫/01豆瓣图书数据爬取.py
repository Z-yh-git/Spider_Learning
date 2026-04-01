
'''
豆瓣图书多页数据爬取：
1.网址规律+请求头
2.发起请求
3.解析数据+提取
4.保存数据（表格） excel/CSV
'''


'''引入请求、bs4解析、pandas、csv库'''
import requests
from bs4 import BeautifulSoup
import pandas
import csv



'''请求头、请求网址的输入'''
h = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
}
bookdatas = []
for i in range(0,226,25):
    url = f"https://book.douban.com/top250?start={i}"

    '''发送请求'''
    response = requests.get(url = url, headers=h)
# print(response)  <Response [200]>请求成功


    '''解析数据'''
    result = BeautifulSoup(response.text, "html.parser")
# print(result)   成功
    title = result.title.text
# print(title)    豆瓣读书 Top 250

    tds =result.find_all('tr',class_ = 'item')
# print(tds)
    for td in tds:
        bookdata = {
            "书名":td.find('div',class_ = 'pl2').find('a').text.strip(),
            "图书信息":td.find('p',class_ = 'pl').text,
            "评分":td.find('span',class_ = 'rating_nums').text,
            "金句":td.find('span',class_ = 'inq').text,
        }

        # print(bookdata["书名"])
        bookdatas.append(bookdata)
# print(bookdatas)
'''
此处是重点：
寻找数据要用循环，对每一个标签下的数据查找
不可以在tds之后用变量继续接收再查找，会报错未解析
尽量一级一级找，尤其对于a标签，否则会找不到
'''


df = pandas.DataFrame(bookdatas)
df.to_excel("01数据/豆瓣图书excel数据.xlsx",index = False)

# 注意:csv 的存储要用with open写入模式
keys =bookdatas[0].keys()
with open('01数据/豆瓣图书CSV数据.csv','w',newline="",encoding="UTF-8") as f:
    csv1 = csv.DictWriter(f, keys)
    csv1.writeheader()
    csv1.writerows(bookdatas)

keys =bookdatas[0].keys()
with open(f'01数据/{title}.csv','w',newline="",encoding="UTF-8") as f:
    csv1 = csv.DictWriter(f, keys)
    csv1.writeheader()
    csv1.writerows(bookdatas)




