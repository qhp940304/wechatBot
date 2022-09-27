# 根据备注发送节日祝贺，没备注的不发
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
        self.sendTxt = '节日祝福'

    def send(self):
        contacts = self.tool.getContacts()
        self.all = len(contacts)
        for k, v in contacts.items():
            if v['remark']:
                self.now += 1
                self.friend = v['remark']
                # wechat.send_text(to_wxid=k, content=v['remark']+self.sendTxt)
                time.sleep(0.3)
    def showTqdm(self):
        last = 0
        with tqdm(total=self.all, unit='人') as pbar:
            while self.now < self.all:
                pbar.set_description(f"正在给【{self.friend}】发送({self.now}/{self.all})")
                pbar.update(self.now - last)
                last = self.now
            pbar.update(self.all - self.now)


def start(_wechat):
    try:
        threads = []
        auto = Holiday(_wechat)

        for x in range(1):
            # 创建线程，并加入容器
            threads.append(threading.Thread(target=auto.showTqdm))
            threads.append(threading.Thread(target=auto.send))
        for t in threads:
            # 启动所有线程
            t.start()
        for t in threads:
            # 主线程等待进程池中的所有线程执行完毕，避免成为孤儿进程
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
        exit(0)
