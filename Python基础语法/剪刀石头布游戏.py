'''
@file:剪刀石头布游戏.py
@author:Vitas
@version:1.0
@intro:实现和用户进行剪刀石头布的游戏
@notice:null
'''
'''
steps:
1.创建列表，包含所有可能
2.随机抽取，并且获得用户的输入
3.比较，得出结果
'''
import random

pool = ["剪刀","石头","布"]
while(1):
    s1 = random.choice(pool)
    s2 = input("请选择你出什么")
    if s1 == s2:
        print("平局")
    elif (s1 == "剪刀" and s2 == "石头") or (s1 == "石头" and s2 == "布") or (s1 == "布" and s2 == "剪刀"):
        print ("你胜出")
        break
    else :
        print("你落败")
        break


