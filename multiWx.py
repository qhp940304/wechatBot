# 微信多开
from ntchat import WeChat
n = input('请输入要打开的微信数量：')
for i in range(int(n)):
    wechat = WeChat()
    wechat.open(smart=False)
txt = ' 打开完成，现在可以关闭本程序 By公众号：嘿python '
_len = len(txt)*2
print('\n',txt.center(_len,' '))
