# encoding:utf-8
# 性别分析

import matplotlib.pyplot as plt
import pandas as pd


def csv_to_list(path):  # 创造一个函数，接受本地已经存在的csv文件的路径作为参数

    data_frame = pd.read_csv(path)  # 读取已经存在的csv文件

    df_list = []  # 创建一个空列表，用于存放最后以字典形式存在的所有好友的信息
    for i in data_frame.index.values:  # 遍历表格中所有的行

        # loc为按列名索引, iloc为按位置索引，使用的是 [[行号], [列名]]
        # data_frame.columns表示读出表格的所有横向标头
        # to_dict()方法表示将前面的数据构造成字典
        df_line = data_frame.loc[i, data_frame.columns].to_dict()

        df_list.append(df_line)  # 将每一行转换成字典后添加到列表

    return df_list  # 返加包含有所有好友信息的列表作为函数值


friends = csv_to_list('we_chat_list.csv')  # 将包含好友信息的csv文件路径作为参数传给函数

# 遍历好友字典，对不同性别计数
sexDict = {}
for friend in friends:

    if friend['Sex'] not in sexDict:
        sexDict[friend['Sex']] = 0
    sexDict[friend['Sex']] += 1

# 不男不女性别数量赋值给变量
unkown = sexDict[0]
# 男性数量赋值给变量
male = sexDict[1]
# 女性数量赋值给变量
female = sexDict[2]

# 字体
plt.rcParams['font.sans-serif'] = ['SimHei']
# 各块颜色
colors = ['yellowgreen', 'lightskyblue', 'lightcoral']
# 饼状图外侧显示的说明文字
labels = ['未知', '男性', '女性']
# 离开中心的距离，用于突出显示其中几块
explode = (0, 0.05, 0.)
# 标题
plt.title('微信好友性别比例')
# 绘制饼图的函数
plt.pie([unkown, male, female], labels=labels, explode=explode, colors=colors, autopct='%1.1f%%')
# 输出到文件
plt.savefig('Sex_Pie.png')
# 显示饼状图
plt.show()

