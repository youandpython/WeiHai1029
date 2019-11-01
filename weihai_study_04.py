# encoding:utf-8
# 词云
import itchat
import numpy as np
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from PIL import Image  #
from jieba import analyse
from pandas.core.frame import DataFrame
import re
import jieba
import matplotlib.pyplot as plt

itchat.auto_login(hotReload=True)
friends = itchat.get_friends(update=True)[1:]

dt = DataFrame(friends)
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


