'''
@file:幸运抽奖.py
@author:Vitas
@version:1.0
@intro:实现与用户互动的抽奖
@notice:null
'''

'''
1.设置奖池和用户的抽奖次数
2.游戏规则介绍
3.开始抽奖
（1）随机抽取并累加奖金，次数减少
（2）询问用户是否继续
（3）抽到炸弹直接清零并退出
'''

import random

#1.设置奖池和用户的抽奖次数
money = [100]*2 + [50]*5 + [20]*7 + [10]*10 + [5]*15 + [1]*20
boom = ["炸弹"]*15
benfit = ["增益"]*5
pool = money + boom + benfit
count = 10

#2.游戏规则介绍
print(f"欢迎来到幸运抽奖游戏，在游戏中你一共有\033[31m{count}\033[0m次机会可以抽奖，奖池中有奖金、炸弹和增益")
print(f"抽中的奖金可以累加，每回合结束都会询问是否继续，若抽到炸弹则奖金清零并退出游戏，抽到增益则加一次抽奖机会")
choice1 = input("请仔细阅读规则，阅读完后请选择是否开始抽奖，请选择是或否")
if choice1 == "否":
    print("退出游戏成功")
elif choice1 == "是":
    print("游戏开始")
    sum = 0
    while(1):
        choice2 = input ("是否抽奖")
        if choice2 == "是":
            result = random.choice(pool)
            if result == "炸弹" :
                print("很遗憾，你抽到了炸弹，游戏结束")
                sum = 0
                break
            elif result == "增益" :
                print("恭喜你抽中增益")
                count += 1
                print(f"你现在有{sum}元，{count}次机会")
            else :
                sum += result
                count -= 1
                print(f"恭喜你抽中{result}元，现在你有{sum}元，{count}次机会")
        else :
            print(f"游戏退出，你获得了{sum}元")






