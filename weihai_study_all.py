# encoding:utf-8
# By Zhang Bohua, from Weifang Shandong
# 将前面代码合成
import itchat
import numpy as np
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from PIL import Image  #
from jieba import analyse
import pandas as pd
import seaborn as sns  # Seaborn是基于matplotlib的图形可视化python包。它提供了一种高度交互式界面，便于用户能够做出各种有吸引力的统计图表。
import re
import jieba
import matplotlib.pyplot as plt

# 形成一个二维码，微信扫描后，模拟登录网页版微信。传入hotReload=True，生成一个静态文件itchat.pkl ，用于存储登陆的状态，不有每次运行都登录。
itchat.auto_login(hotReload=True)
# 返回完整的好友列表，每个好友为一个字典, 其中第一项为本人的账号信息。传入update=True, 将更新好友列表并返回。
friends = itchat.get_friends(update=True)[1:]  # [1:]表示切片，除掉第一项也就是本人的账号信息。
# DataFrame是pandas库的一个类，我们通过调用DataFrame()创建一个对象实例。是一种类似于excel的数据结构，是一种二维表，单元格可以存放数值、字符串等。
# data = DataFrame(friends)
data = pd.DataFrame(friends)
data.to_csv('we_chat_list.csv', encoding='utf_8_sig')


def sex_pie():
    # 遍历好友字典，对不同性别计数
    sex_dict = {}
    # total = len(friends)
    for friend in friends:
        if friend['Sex'] not in sex_dict:
            sex_dict[friend['Sex']] = 0
        sex_dict[friend['Sex']] += 1

    # 不男不女性别数量赋值给变量
    unknow = sex_dict[0]
    # 男性数量赋值给变量
    male = sex_dict[1]
    # 女性数量赋值给变量
    female = sex_dict[2]

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
    plt.pie([unknow, male, female], labels=labels, explode=explode, colors=colors, autopct='%1.1f%%')
    # 输出到文件
    plt.savefig('Sex_Pie.png')
    # 显示饼状图
    plt.show()


def province_bar(division):
    # 6个默认的颜色循环主题： deep, muted, pastel, bright, dark, colorblind
    # desat：每种颜色去饱和的比例
    # 设置调色板
    sns.set_palette('deep', desat=.8)
    # 设置rc参数显示中文标题，设置字体为SimHei显示中文。 rc：run configuration。
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 从Province（省份）为山东的列中将City对应的城市进行计数。
    # value_counts()是一种查看表格某列中有多少个不同值的快捷方法，并计算每个不同值有在该列中有多少重复值。
    counters = None
    if division == '中国':
        counters = data['Province'].value_counts()
    if division != '中国':
        counters = data[data['Province'] == division]['City'].value_counts()

    counters = counters.sort_values(ascending=False)

    length = 6  # 预设柱状图显示6个城市
    if len(counters) > length:
        counters, temp = counters[:length], counters[length:]  # 给变量命名的另外一种方式
        value = sum(temp)  # 将length数量之外的城市数量求和
        counters['其他'] = value  # 在Series(可理解为字典）中插入一组数据（键值对）
    # bar是柱状图函数，counters.index表示X轴（横坐标）、counters表示Y轴（纵坐标）。
    plt.bar(counters.index, counters)
    # 标题
    plt.title('微信好友区划分布图')
    # 输出到文件
    plt.savefig('City_Bar.png')
    # 显示柱状图
    plt.show()


def signature_word_cloud():
    itchat.auto_login(hotReload=True)
    friends = itchat.get_friends(update=True)[1:]

    # dt = pd.DataFrame(friends)
    # dt.to_csv('ok.csv', encoding='utf_8_sig', header=True, index=True)

    signatures = ''
    for friend in friends:
        signature = friend['Signature']
        if len(signature) == 0:
            continue
        signature = signature.strip().replace('span', '').replace('class', '').replace('emoji', '')  # 去除⽆关数据
        signature = re.sub(r'1f(\d.+)', '', signature)
        signatures += ' '.join(jieba.analyse.extract_tags(signature))  # 关键字提取
        signatures += ' '

    # Image.open，读取指定图片。
    im = Image.open('hbz.jpg')  # 可替换你喜欢的图⽚，在当前文件夹下（相对路径）
    # np.array，将读入的im转换成背景图数据。
    mask = np.array(im)
    # WordCloud函数，建立词云对象
    # mask参数用于设置词云形状，默认的是矩形，可以读入自己选定的图片。margin：画布偏移，默认2像素.
    word_cloud = WordCloud(font_path='simhei.ttf', background_color='white', max_words=1200, mask=mask, margin=15)
    # generate，向word_could这个WordCloud对象中加载signatures（文本内容），对全部文本进行自动分词（但是对中文支持不好）
    word_cloud.generate(signatures)
    # ImageColorGenerator函数通过mask参数生成词云颜色值
    image_colors = ImageColorGenerator(mask)
    # 用recolor方法重置词云颜色为（color_func=image_colors）
    word_clour = word_cloud.recolor(color_func=image_colors)
    # figure函数中，figsize表示输出的绘图对象的宽和高、dpi表示指定绘图对象的分辨率，即每英寸多少个像素，缺省值为80。
    plt.figure(figsize=(12, 12), dpi=100)
    # imshow函数用于对按照样本图片重置颜色的图像进行处理，并显示其格式，但是不能显示。
    plt.imshow(word_clour)
    # 不显示坐标尺寸
    plt.axis('off')
    # 显示词云图
    plt.show()
    # 输出到文件
    word_cloud.to_file('signatures.png')


while True:
    flag = input('________________________________________\n'
                 'Please press the letter:\n'
                 'Press the \'s\' to sex_pie_chart.\n'
                 'Press the \'p\' to province_bar_chart.\n'
                 'Press the \'w\' to signature_word_cloud.\n'
                 'Press the \'e\' to exit.\n'
                 '_________________________________________')
    try:
        if flag == 's':
            sex_pie()

        if flag == 'p':
            division = input('Please input the division:')
            if division == '':
                division = '中国'
            province_bar(division)

        if flag == 'w':
            signature_word_cloud()

        if flag == 'e':
            break
    except ValueError:
        pass

print('\n*******************************************\n'
      '* Thank you for coming, you are the best. *\n'
      '*******************************************')




