'''
@file:学生管理系统.py
@author:Vitas
@version:1.0
@intro:显示、添加、删除、修改、排序学生的数据
@notice:null
'''
'''
steps:
1.创建数据
2.封装实现特定的函数
'''
# 原始数据
datas = [
    {
        'id': 1,
        '姓名':'张三',
        '年级':'高三',
        '分数':605.0
    },
    {
        'id': 2,
        '姓名':'李四',
        '年级':'高三',
        '分数':630.0
    },
{
        'id': 3,
        '姓名':'王五',
        '年级':'高三',
        '分数':598.5
    },

]

# 封装函数
# (1)展示学生信息函数
def Show ():
    for data in datas:
        print(data)

# (2)添加学生信息函数
def Add():
    extra = {#注意别忘记取变量名
        'id': int(input("请输入输入学生的id")),
        '姓名': input("请输入输入学生的姓名"),
        '年级': input("请输入输入学生的年级"),
        '分数': float(input("请输入输入学生最近一次考试的分数"))
            }
    datas.append(extra)
    print("更新后的学生全体学生信息为：")
    Show()

# (3)删除学生信息函数
def Delete():
    Show()
    d1 = int(input("请选择需要删除的学生id"))
    for i in datas:
        if i['id'] == d1:
            datas.remove(i)#对于嵌套结构，先遍历再进行之后的操作永远是一个好的思路
    print("更新后的学生全体学生信息为：")
    Show()

# (4)修改学生信息函数
def Change():
    Show()
    c1 = int(input("请选择需要修改的学生id"))
    for i in datas:
        if i['id'] == c1:
            print("已找到需要修改信息的学生")
            print(i)
            while (1) :
                c2 = int(input("请选择需要修改的内容：1.id 2.姓名 3.年级 4.分数 5.退出修改程序"))
                if c2 == 1:
                    id = int(input("请输入学生的id"))
                    i['id'] = id
                    print("更新后的学生信息为：")
                    print(i)
                if c2 == 2:
                    Newname = input("请输入学生的名字")
                    i['姓名'] = Newname
                    print("更新后的学生信息为：")
                    print(i)
                if c2 == 3:
                    Newgrade = input("请输入学生的年级")
                    i['年级'] = Newgrade
                    print("更新后的学生信息为：")
                    print(i)
                if c2 == 4:
                    Newscore = float(input("请输入学生的分数"))
                    i['分数'] = Newscore
                    print("更新后的学生信息为：")
                    print(i)
                if c2 == 5:
                    print("已成功退出")
                    print("更新后的学生全体学生信息为：")
                    Show()
                    break

# (5)排名函数
def rank():
    datas.sort(key = lambda i: i['分数'],reverse = True)
    print("更新后的学生全体学生信息为：")
    Show()

print("您已成功进入学生管理系统，你可以进行如下操作")
while(1):

    # 获取用户选择
    print("1.查看全体学生信息 2.添加学生信息 3.删除学生信息 4.修改学生信息 5.对学生信息按成绩排序 6.退出系统")
    ans = int(input("请输入你的选择"))
    # 流程进入
    if ans == 1:
        Show()
    elif ans == 2:
        Add()
    elif ans == 3:
        Delete()
    elif ans == 4:
        Change()
    elif ans == 5:
        rank()
    elif ans == 6:
        break


