'''
要求：1.爬取电影名、信息、评分
2.使用Xpath语法
3.保存为excel和CSV格式表格
4.应用os库自动创建文件夹
步骤:
1.确定请求头、url
2.发送请求、获取数据
3.解析、提取数据
4.保存
'''
import csv

#爬虫库
import requests
#Xpath解析库
from lxml import etree
#存储数据库
import os
import pandas as pd
# 线程池
from concurrent.futures import ThreadPoolExecutor
#时间库
import time

#请求网址和请求头准备
urls = []
for i in range(0,226,25):
    url = f"https://movie.douban.com/top250?start={i}&filter="
    urls.append(url)
h = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
    }


# 打包爬虫函数
def spider1(url):
    print("开始任务")
    '''发送请求'''
    data1 = requests.get(url, headers=h)
    # print(data1)<Response [200]>
    '''数据解析、提取'''
    result = etree.HTML(data1.text)
    title = result.xpath('//div[@id="content"]/h1/text()')
    # print(title)返回的是列表
    data2 = result.xpath('//ol[@class="grid_view"]/li')
    # print(data2)获取到了
    datas = []
    for d in data2:
        data = {
            "图片地址": d.xpath('.//img/@src'),
            "电影名":d.xpath('.//div[@class = "hd"]//span[@class="title"]/text()'),
            "别名":d.xpath('.//div[@class = "hd"]//span[@class="other"]/text()'),
            "电影信息":d.xpath('.//div[@class = "bd"]/p/text()'),
            "评分":d.xpath('.//div[@class = "bd"]//span[@class = "rating_num"]/text()'),
            "金句":d.xpath('.//p[@class = "quote"]/span/text()'),
        }
        datas.append(data)
    # for i in datas:
    #     print(i)
    '''数据保存'''
    keys = datas[0].keys()
    if not os.path.exists('02数据'):
        os.mkdir("02数据")

    pds = pd.DataFrame(datas)
    pds.to_excel("02数据/单线程豆瓣电影excel多页数据.xlsx", index=False)

    with open ("02数据/单线程豆瓣电影csv多页数据.csv","w",encoding="utf-8") as f:
        csvs = csv.DictWriter(f,keys)
        csvs.writeheader()
        csvs.writerows(datas)


print("单线程开始执行")
start_time1 = time.time()
for url in urls:
    spider1(url)
times1 = '%.4f'%(time.time() - start_time1)
print(f"执行完毕，用时{times1}秒")#用时5.1446秒

def spider2(url):
    print("开始任务")
    '''发送请求'''
    data1 = requests.get(url, headers=h)
    # print(data1)<Response [200]>
    '''数据解析、提取'''
    result = etree.HTML(data1.text)
    title = result.xpath('//div[@id="content"]/h1/text()')
    # print(title)返回的是列表
    data2 = result.xpath('//ol[@class="grid_view"]/li')
    # print(data2)获取到了
    datas = []
    for d in data2:
        data = {
            "图片地址": d.xpath('.//img/@src'),
            "电影名":d.xpath('.//div[@class = "hd"]//span[@class="title"]/text()'),
            "别名":d.xpath('.//div[@class = "hd"]//span[@class="other"]/text()'),
            "电影信息":d.xpath('.//div[@class = "bd"]/p/text()'),
            "评分":d.xpath('.//div[@class = "bd"]//span[@class = "rating_num"]/text()'),
            "金句":d.xpath('.//p[@class = "quote"]/span/text()'),
        }
        datas.append(data)
    # for i in datas:
    #     print(i)
    '''数据保存'''
    keys = datas[0].keys()
    if not os.path.exists('02数据'):
        os.mkdir("02数据")

    pds = pd.DataFrame(datas)
    pds.to_excel("02数据/多线程豆瓣电影excel多页数据.xlsx", index=False)

    with open ("02数据/多线程豆瓣电影csv多页数据.csv","w",encoding="utf-8") as f:
        csvs = csv.DictWriter(f,keys)
        csvs.writeheader()
        csvs.writerows(datas)


print("多线程开始执行")
start_time2 = time.time()
with ThreadPoolExecutor (max_workers=5) as executor:
    executor.map(spider2, urls)
times2 = '%.4f'%(time.time() - start_time2)#保留四位小数，理解：.nf表示取n位小数，%用来指代需要做出此操作的对象
print(f"执行完毕，用时{times2}秒")#用时1.3643秒



