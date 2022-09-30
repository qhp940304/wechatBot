# 根据备注发送节日祝贺，没备注的不发
# self.sendTxt为节日祝福语，要自己写
import sys
import threading
import time

import tools
from tqdm import tqdm
import ntchat


class Holiday:
    def __init__(self, wechat):
        self.wechat = wechat
        self.tool = tools.Tools(wechat)
        self.all = 1
        self.now = 0
        self.friend = ''
        self.sendTxt = '这里写你的节日祝福'
        # 休眠几秒再发下一个人，根据自己实际情况修改
        self.sleep = 3
    def send(self):
        contacts = self.tool.getContacts()
        contacts = {k: v for k, v in contacts.items() if v['remark']}
        self.all = len(contacts)
        for k, v in contacts.items():
            if v['remark']:
                self.now += 1
                self.friend = v['remark']
                # 测试完成后，打开下面的注释，就可以正式发送了
                # wechat.send_text(to_wxid=k, content=f"{v['remark']},{self.sendTxt}")
                # 休眠几秒再发下一个人
                time.sleep(self.sleep)

    def showTqdm(self):
        last = 0
        with tqdm(total=self.all, unit='人') as pbar:
            while self.now < self.all:
                pbar.set_description(f"正在给【{self.friend}】发送({self.now}/{self.all})")
                pbar.update(self.now - last)
                last = self.now
            pbar.update(self.all - self.now)
        print('Done')

def start(_wechat):
    try:
        threads = []
        auto = Holiday(_wechat)

        for x in range(1):
            # 创建线程，并加入容器
            threads.append(threading.Thread(target=auto.showTqdm))
            threads.append(threading.Thread(target=auto.send))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    except Exception as e:
        print('发生异常：', e)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        ntchat.exit_()
        sys.exit()


if __name__ == '__main__':
    wechat = ntchat.WeChat()
    try:
        wechat.open(smart=True)
        # 等待登录
        wechat.wait_login()
        start(wechat)
    except Exception as e:
        print('微信版本不对应，请在公众号(嘿python)下载指定版本微信', e)
        ntchat.exit_()
        sys.exit()
