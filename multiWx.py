# 微信多开
from ntchat import WeChat
import sys
import ntchat
def start():
    argv = sys.argv
    # 支持传入文件方式添加好友
    n = argv[-1] if len(argv) > 2 else 1

    for i in range(int(n)):
        wechat = WeChat()
        wechat.open(smart=False)
    txt = ' 打开完成，现在可以关闭本程序 By公众号：嘿python '
    _len = len(txt) * 2
    print('\n', txt.center(_len, ' '))
    try:
        while True:
            pass
    except KeyboardInterrupt:
        ntchat.exit_()
        sys.exit()