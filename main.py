import random
import sys
import time

import ntchat

'''
群机器人
私聊机器人(自动回复消息，自动回复关键词消息[例如节日祝福])
加群好友(不加群主)
分析群属性
防撤销
'''

sleepMin = 1
sleepMax = 60
wechat = ntchat.WeChat()
# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)
# 等待登录
wechat.wait_login()
# 向文件助手发送一条消息
wechat.send_text(to_wxid="filehelper", content="ntchat登陆成功")

# 获取好友信息
def getContacts():
    contacts = {v['wxid']: v for k, v in enumerate(wechat.get_contacts())}
    # print(contacts)
    return contacts


# 选择要加的成员群
def choiceRooms(rooms):
    addRooms = input('请输入要加的群成员，用逗号分隔,例如：1,10,18 输入完成后敲回车')
    # 避免连敲回车
    while not addRooms:
        print('addrooms', addRooms)
        addRooms = input('请输入要加的群成员，用逗号分隔,例如：1,10,18 输入完成后敲回车')

    addRooms = addRooms.replace('，', ',').replace(' ', '').split(',')
    print(addRooms)
    print(rooms)
    print('您要加的成员群为：')
    print('==============================')
    for item in addRooms:
        x = int(item)
        if x < len(rooms):
            print('|| ', rooms[x]['nickname'])
        else:
            print(x, ':序号不存在')
    if input('输入n重新选择,y继续').lower() == 'n':
        choiceRooms(rooms)
    else:
        addRooms = [v for k, v in enumerate(rooms) if str(k) in addRooms]
        return addRooms


# 添加指定群内的成员(不加管理员)
def addRoomsFreiends(addRooms, contacts, sleepMin=1, sleepMax=60):
    verifyTxt = input('请输入：添加好友时的验证消息')
    for room in addRooms:
        print('开始添加群：', room)
        # 遍历群成员
        for friends in room['member_list']:
            print('执行添加：', friends)
            if friends != room['manager_wxid'] and friends not in contacts:
                addRes = wechat.add_room_friend(
                    room_wxid=room['wxid'],
                    wxid=friends,
                    verify=verifyTxt
                )
                print('添加情况：', addRes)
                sleepRand = random.randint(sleepMin, sleepMax)
                print(f'{sleepRand}秒后添加下一位好友')
                time.sleep(sleepRand)
            else:
                print('好友或管理员，略过：', friends)
        print(room['nickname'], '群内所有成员添加完成')
    print('\n\n\n\n！！！！！！！所有的群添加完成！！！！！！！！！\n\n\n\n')


# 获取群信息
rooms = wechat.get_rooms()
try:
    for k, v in enumerate(rooms):
        print(f"序号：{k} >>> 群名：{v['nickname']}")
    print('\n')
    # 获取群
    addRooms = choiceRooms(rooms)
    # 获取好友列表
    contacts = getContacts()
    # 添加指定群内成员
    addRoomsFreiends(addRooms, contacts)
except Exception as e:
    print('发生异常：', e)


# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    print('收到消息', message)
    from_wxid = data["from_wxid"]
    self_wxid = wechat_instance.get_login_info()["wxid"]

    # 判断消息不是自己发的，并回复对方
    # if from_wxid != self_wxid:
    #     wechat_instance.send_text(to_wxid=from_wxid, content=f"自动回复：你发送的消息是: {data['msg']}")


try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
