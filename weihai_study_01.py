# encoding:utf-8
# 抓取微信好友信息，保存到本地。
import itchat
from pandas.core.frame import DataFrame

# 形成一个二维码，微信扫描后，模拟登录网页版微信。传入hotReload=True，生成一个静态文件itchat.pkl ，用于存储登陆的状态，不有每次运行都登录。
itchat.auto_login(hotReload=True)
# 返回完整的好友列表，每个好友为一个字典, 其中第一项为本人的账号信息。传入update=True, 将更新好友列表并返回。
friends = itchat.get_friends(update=True)[1:]  # [1:]表示切片，除掉第一项也就是本人的账号信息。

# DataFrame是pandas库的一个类，我们通过调用DataFrame()创建一个对象实例。是一种类似于excel的数据结构，是一种二维表，单元格可以存放数值、字符串等。
data = DataFrame(friends)

'''
to_csv()是DataFrame类的方法.
CSV格式比Excel格式具备的优势：
1）CSV是纯文本文件，支持追加模式写入，节省内存。Excel是结构复杂的二进制文件，只支持一次性写入，较费内存。
2）CSV的文件行数没有限制，在实际项目中我们已输出过上千万行的CSV文件；32位系统下Excel单个Sheet最多支持65535行。
3）CSV是纯文本文件，可以使用任何文本编辑器进行编辑，因此可以在Linux终端下对其进行修改。Excel是二进制文件，目前已知的编辑工具有Office，OpenOffice，WPS，都为GUI工具，不支持在终端下编辑。
'''
data.to_csv('we_chat_list.csv', encoding='utf_8_sig')


