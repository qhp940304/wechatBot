import json
import random
import sys

import ntchat
from time import sleep

# 先加小号为好友
# 通过加好友入群方式测试是否被删除
# 将小号加入群，小号可以加群成员为好友
# 可以获取到所有好友列表，通过接口发送到服务器
sleepMin = 1
sleepMax = 20
wechat = ntchat.WeChat()
# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)
# 等待登录
wechat.wait_login()
# 向文件助手发送一条消息
wechat.send_text(to_wxid="filehelper", content="即将开始测试单删")
sendTxt = '单删测试'
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
    # 贾斯丁比巴卜 wxid_j39yy6ryigzw22
    # q wxid_0s3gctqf9wy012
    if k == 'wxid_0s3gctqf9wy012':
        sendRes = wechat.send_text(to_wxid=k, content=sendTxt)
        print('发送结果：', sendRes)
        sleep(random.randint(sleepMin, sleepMax))
print('-------------------单删测试完成-----------------------')
isDel = {}
with open('D:/test.log', 'r', encoding='utf-8') as f:
    # line = f.readline()  # 调用文件的 readline()方法，一次读取一行
    strSign = '开启了朋友验证，你还不是他（她）朋友'
    while line := f.readline():
        if strSign in line:
            print(line)
            start = line.index("{'data': {")
            end = line.rindex(' ')
            strs = line[start:end].replace("'", '"').replace('="', "='").replace('">', "'>")
            print(strs)
            strJson = json.loads(strs)['data']
            print(strJson)
            print(type(strJson))
            wxid = strJson['from_wxid']
            end = strJson['raw_msg'].index(strSign)
            nickName = strJson['raw_msg'][:end]
            print(wxid, nickName)
            isDel[wxid]=nickName
        # line = f.readline()
    print('分析完成')
    if isDel:
        print('被单删好友如下：')
        for k,v in isDel.items():
            print(v)
        print('已将他们他们排序在前，您可以去微信上删除他们')
        goDel = input('是否删除他们？删除(y)，不删除(n)').lower()
        if goDel=='y':
            print('ntchat不支持删除')
        else:
            print('Bye')
    else:
        print('恭喜，没有被单删的好友')
        roomTest = wechat.create_room(list(isDel.keys()))
# print(roomTest)


try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
