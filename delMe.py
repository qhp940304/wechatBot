import random
import sys

import ntchat
from time import sleep

sleepMin = 1
sleepMax = 20
wechat = ntchat.WeChat()
# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)
# 等待登录
wechat.wait_login()
# 向文件助手发送一条消息
wechat.send_text(to_wxid="filehelper", content="即将开始测试单删")
# 被删除的好友
deled = []


def getContacts():
    contacts = {v['wxid']: v for k, v in enumerate(wechat.get_contacts())}
    # print(contacts)
    return contacts


contacts = getContacts()
# print(contacts)
friends = len(contacts)
timeMin = int(friends * sleepMin / 60)
timeMax = int(friends * sleepMax / 60)
print(f'程序即将开始，运行时间大概为{timeMin}-{timeMax}分钟')
for k, v in contacts.items():
    # print(k,v)
    if k == 'wxid_0s3gctqf9wy012':
        sendRes = wechat.send_text(to_wxid=k, content=f'单删测试')
        print('单删结果：', sendRes)
        sleep(random.randint(sleepMin, sleepMax))
print('-------------------单删测试完成-----------------------')

try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
