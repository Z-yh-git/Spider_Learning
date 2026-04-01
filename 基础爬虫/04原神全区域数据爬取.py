'''
要求：1.爬取全区域角色数据
2.合理解析提取数据（Json），数据越多越好
3.保存至表格
'''

import requests
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor


'''确定请求头、网址'''
h = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
}
datas = []
def spider(url_single):
    response = requests.get(url_single, headers=h)
    # print(response)<Response [200]>

    '''数据解析'''
    result = json.loads(response.text)
    d1 = result["data"]["list"]
    # print(d1)
    for i in d1:
        character = {
            "姓名": i["sTitle"],
        }
        info = json.loads(i["sExt"])
        # print(info)
        character["UI图片"] = info["732_0"][0]["url"]
        character["PC端图片"] = info["732_1"][0]["url"]
        character["移动端图片"] = info["732_15"][0]["url"]
        character["中文配音"] = info["732_5"]
        character["日文配音"] = info["732_6"]
        character["台词"] = info["732_7"]
        datas.append(character)
        # character["图片地址"] = info["url"]
        datas.append(character)
        # print("执行完成")
urls = []
for i in range(727, 733, 1):
    url = f"https://act-api-takumi-static.mihoyo.com/content_v2_user/app/16471662a82d418a/getContentList?iAppId=43&iChanId={i}&iPageSize=50&iPage=1&sLangKey=zh-cn&iOrder=6"
    spider(url)
    print("执行完成")


url_extra ="https://act-api-takumi-static.mihoyo.com/content_v2_user/app/16471662a82d418a/getContentList?iAppId=43&iChanId=1219&iPageSize=50&iPage=1&sLangKey=zh-cn&iOrder=6"
spider(url_extra)
print("执行完成")



# with ThreadPoolExecutor(max_workers=6) as executor:
#     executor.map(spider, urls)



ds = pd.DataFrame(datas)
ds.to_excel("04数据/原神全区域数据.xlsx", index=False)
