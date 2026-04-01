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


