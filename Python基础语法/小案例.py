'''
1.求1-100之间的奇数之和
'''
sum = 0
for i in range(1,101,2):
    sum += i
print(sum)



'''2.
请分别统计每个学生的总分和平均分，以字典的形式输出
score = {
    "张三":{"语文":90,"数学":85,"英语":92},
    "李四":{"语文":72,"数学":95,"英语":88},
    "王五":{"语文":85,"数学":78,"英语":90},
}
输出内容如下：
{"张三":{"总成绩":xxx,"平均成绩":xxx},"李四":{"总成绩":xxx,"平均成绩":xxx}....}
'''
score = {
    "张三":{"语文":90,"数学":85,"英语":92},
    "李四":{"语文":72,"数学":95,"英语":88},
    "王五":{"语文":85,"数学":78,"英语":90},
}
for u,v in score.items():#要先将字典强转为列表嵌套元组的形式，否则拿不到值
    # print(u,v)
    Chinese = v["语文"]
    # print(chinese)
    math = v["数学"]
    English = v["英语"]
    all = Chinese+math+English
    average = all/len(v)
    print(f"{u}的总成绩是{all}，平均成绩是{'%.2f' %average}")

'''
作业3:必做(难易程度**)
编写一个名为collatz()的函数,它有一个名为number的参数
如果参数是偶数,那么collatz()就打印出偶数
如果number是奇数,collatz()就打印奇数
'''
def collatz(number):
    if number % 2 == 0:
        print("偶数")
    else:
        print("奇数")
collatz(100)


'''
4.九九乘法表
'''
#1.外层为所有行数
#2.内层为列数，且列数小于等于行数

for i in range(1,10):
    for j in range(1,i+1):
        print(f"{j}*{i}={i*j}   ",end="")#内层要适用end参数来取消换行
    print()#打印完每一行之后要换行

