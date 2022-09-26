from sys import argv

import ntchat

import AutoAddPhone
import AutoAddRoomsFreiends
import OneWay
import multiWx
import tools

_str = '**************************************\n' \
       '* 载入中...                          *\n' \
       '* 本工具支持【免费定制】             *\n' \
       '* 有问题或建议请联系公众号：嘿python *\n' \
       '**************************************\n'
print(_str)
# 获取群信息
wechat = ntchat.WeChat()
try:
    wechat.open(smart=True)
    # 等待登录
    wechat.wait_login()
except Exception as e:
    print('微信版本不对应，请在公众号(嘿python)下载指定版本微信', e)
    exit(0)
tool = tools.Tools(wechat)
# 鉴权
tool.sCon()
can = tool.canUse()
if not can:
    print('免费获取使用权\n请联系公众号:嘿python')
    exit(0)
menu = '*****************************************************\n' \
       '* 参数错误(有问题联系公众号:嘿python)               *\n' \
       '*****************************************************\n' \
       '* 参数应为：功能 参数（注意功能和参数之间有个空格） *\n' \
       '* 1 自动添加群好友                                  *\n' \
       '* 2 自动添加好友                                    *\n' \
       '* 3 测试单向好友                                    *\n' \
       '* 4 多开                                            *\n' \
       '*****************************************************\n' \
       '* 例如：                                            *\n' \
       '*     自动添加群好友  wxwx 1                        *\n' \
       '*     自动添加好友    wxwx 2                        *\n' \
       '*     添加指定excel的好友 wxwx 2 D:\phone.xlsx      *\n' \
       '*****************************************************\n'

if len(argv) > 1:
    select = int(argv[1])
    if select == 1:

        AutoAddRoomsFreiends.start(wechat)
    elif select == 2:

        AutoAddPhone.start(wechat)
    elif select == 3:

        OneWay.start(wechat)
    elif select == 4:

        multiWx.start()
    else:
        print(menu)
else:
    print(menu)
