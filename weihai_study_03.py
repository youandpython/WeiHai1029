# encoding:utf-8
# 主要分布在哪些省份（城市）
import itchat
import pandas as pd
import matplotlib.pyplot as plt  # Matplotlib是Python中用的最多的2D图形绘图库，学好Matplotlib的用法可以帮助我们在统计分析中更灵活的展示各种数据的状态。
import seaborn as sns  # Seaborn是基于matplotlib的图形可视化python包。它提供了一种高度交互式界面，便于用户能够做出各种有吸引力的统计图表。

itchat.auto_login(hotReload=True)
friends = itchat.get_friends(update=True)[1:]
data = pd.DataFrame(friends)

# 6个默认的颜色循环主题： deep, muted, pastel, bright, dark, colorblind
# desat：每种颜色去饱和的比例
# 设置调色板
sns.set_palette('deep', desat=.8)
# 设置rc参数显示中文标题，设置字体为SimHei显示中文。 rc：run configuration。
plt.rcParams['font.sans-serif'] = ['SimHei']
# 从Province（省份）为山东的列中将City对应的城市进行计数。
# value_counts()是一种查看表格某列中有多少个不同值的快捷方法，并计算每个不同值有在该列中有多少重复值。
# counters = data[data['Province'] == '山东']['City'].value_counts()
# 将Province（省份）进行计数。
counters = data['Province'].value_counts()
# ascending为假时降序排列。
counters = counters.sort_values(ascending=False)

length = 6  # 预设柱状图显示6个城市
if len(counters) > length:
    counters, temp = counters[:length], counters[length:]  # 给变量命名的另外一种方式
    value = sum(temp)  # 将length数量之外的城市数量求和
    counters['其他'] = value  # 在Series(可理解为字典）中插入一组数据（键值对）
# bar是柱状图函数，counters.index表示X轴（横坐标）、counters表示Y轴（纵坐标）。
plt.bar(counters.index, counters)
# 标题
plt.title('省内城市微信好友分布图')
# 输出到文件
plt.savefig('City_Bar.png')
# 显示柱状图
plt.show()
