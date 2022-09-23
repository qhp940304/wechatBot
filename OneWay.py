import ntchat as chat
from json import loads as jsonLoads
from random import randint
from sys import exit as sysExit
from threading import Thread as threadingThread
from tqdm import tqdm
import tools
from time import sleep


# wechat = chat.WeChat()


class OneWay:
    def __init__(self):

        self.sleepMin = 1
        self.sleepMax = 20
        # 打开pc微信, smart: 是否管理已经登录的微信
        try:
            wechat.open(smart=True)
            # 等待登录
            wechat.wait_login()
        except Exception as e:
            print('微信版本不对应，请在公众号(嘿python)下载指定版本微信', e)
        # 向文件助手发送一条消息
        self.sendTxt = '打扰了，我在测试单向好友\n' \
                       '谢谢您没删我，ღ( ´･ᴗ･` )比心\n' \
                       '点击下面链接\n' \
                       '免费领取本工具'
        # 单向好友
        self.deled = []
        self.img = 'http://mmbiz.qpic.cn/mmbiz_png/OC3fv21C02EViahTMLwyCn4rgcFYDOOjtic4w4HVJsS5KVOew5SZJT6w9dO14r8gj9dCRLBwickClibzaojRov5xLw/0?wx_fmt=png'
        self.url = 'http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzAwMTA5MTE1OQ==#wechat_webview_type=1&amp;wechat_redirect'

    def run(self):

        contacts = tool.getContacts()
        count = len(contacts)
        i = 0
        try:
            with tqdm(total=count, unit='人') as pbar:
                for k, v in contacts.items():
                    try:
                        i += 1
                        wechat.send_text(to_wxid=k, content=self.sendTxt)
                        wechat.send_link_card(to_wxid=k, title='嘿Python',
                                              desc='公众号名片', url=self.url, image_url=self.img)
                        pbar.set_description(f"进度：({i}/{count})")
                        pbar.update(1)
                        sleep(randint(self.sleepMin, self.sleepMax) / 2)
                    except Exception as e:
                        print('发送消息失败，略过：', e)
                pbar.update(count - i)
        except Exception as e:
            print('error请联系嘿python：', e)
        try:
            print('---------------------------------------------------')
            isDel = {}
            with open('D:/wxntest.log', 'r', encoding='utf-8') as f:
                strSign = '开启了朋友验证，你还不是他（她）朋友'
                while line := f.readline():
                    try:
                        if strSign in line:
                            start = line.index("{'data': {")
                            end = line.rindex(' ')
                            strs = line[start:end].replace("'", '"').replace('="', "='").replace('">', "'>")
                            strJson = jsonLoads(strs)['data']
                            wxid = strJson['from_wxid']
                            end = strJson['raw_msg'].index(strSign)
                            nickName = strJson['raw_msg'][:end]
                            isDel[wxid] = nickName
                    except Exception as e:
                        print('一条错误数据，略过：', e)
                if isDel:
                    print('被单删好友如下：')
                    for k, v in isDel.items():
                        print(v)
                        wechat.send_text(to_wxid=k, content=self.sendTxt)
                    print('已将他们他们排序在前，您可以去微信上删除他们')
                else:
                    print('恭喜，没有单向好友')
                tool.endPrint()
        except Exception as e:
            print('error请联系嘿python：', e)


# if __name__ == '__main__':
tool = ''
wechat = ''


def start(_wechat):
    try:
        global wechat, tool
        wechat = _wechat
        tool = tools.Tools(wechat)
        auto = OneWay()
        threads = []
        uInf = wechat.get_self_info()
        # 记录日志
        tool.log(uInf, 1)
        with open('D:/test.log', 'w', encoding='utf-8') as f:
            f.write('--start--\n')
        for x in range(1):
            # threads.append(threadingThread(target=tool.sCon))
            threads.append(threadingThread(target=auto.run))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        try:
            while True:
                pass
        except KeyboardInterrupt:
            chat.exit_()
            sysExit()
    except Exception as e:
        print('error请联系嘿python：', e)
