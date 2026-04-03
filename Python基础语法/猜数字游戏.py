'''
@file:猜数字游戏.py
@author:Vitas
@version:1.0
@intro:生成一个随机数，引导用户猜
@notice:null
'''
#引入随机库
import random

# 1.生成随机数，获取用户的猜测数字
answer =  random.randint(1,100)
# s1 = int(input("请输入猜测的数字"))

# 2.设置循环，让用户猜数字
while (1) :
    s1 = int(input("请输入猜测的数字"))#每次循环时都要让用户猜一次数字
    if s1 == answer:
        print("恭喜你猜对了")
        break
    elif s1 > answer:
        print("猜大了")
    else  :
        print("猜小了")

