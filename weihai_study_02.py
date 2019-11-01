# encoding:utf-8
# 性别分析
import itchat
import matplotlib.pyplot as plt

itchat.auto_login(hotReload=True)
friend = itchat.get_friends(update=True)[1:]

# 遍历好友字典，对不同性别计数
sexDict = {}
total = len(friend)
for friend in friend:
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

