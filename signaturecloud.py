# encoding:utf-8
# 词云
import numpy as np
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from PIL import Image  #
from jieba import analyse
import pandas as pd
import re
import jieba
import matplotlib.pyplot as plt
import time


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

signatures = ''
for friend in friends:
    signature = friend['Signature']
    if signature == '':
        continue
    signature = str(signature)
    signature = signature.strip().replace('span', '').replace('class', '').replace('emoji', '')  # 去除⽆关数据
    signature = re.sub(r'1f(\d.+)', '', signature)
    signatures += ' '.join(jieba.analyse.extract_tags(signature))  # 关键字提取
    signatures += ' '

# Image.open，读取指定图片。
im = Image.open('photo.jpg')  # 可替换你喜欢的图⽚，在当前文件夹下（相对路径）
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



