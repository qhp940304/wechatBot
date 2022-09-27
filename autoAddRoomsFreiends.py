import random
import sys
import time
import ntchat
from tqdm import tqdm
import tools
import threading

'''
加群好友(不加群主)
'''
sleepFriendMin = 1
sleepFriendMax = 20


class AutoAddRoomsFreiends:
    def __init__(self):
        self.addRooms = []
        self.contacts = []
        self.sleepMin = 1
        self.sleepMax = 60

        # 要添加的群个数
        self.roomsCount = 0
        # 已添加群个数
        self.roomsNow = 1
        # 正在添加群的成员个数
        self.accountCount = 0
        # 已添加成员人数
        self.accountNow = 1
        # 正在添加的群名
        self.roomsName = ''

    # 获取好友信息
    def getContacts(self):
        contacts = {v['wxid']: v for k, v in enumerate(wechat.get_contacts())}
        return contacts

    # 选择要加的成员群
    def choiceRooms(self, rooms):
        addRooms = input('请输入要加的群成员，用逗号分隔,例如：1,10,18 输入完成后敲回车')
        # 避免连敲回车
        while not addRooms:
            # print('addrooms', addRooms)
            addRooms = input('请输入要加的群成员，用逗号分隔,例如：1,10,18 输入完成后敲回车')
        addRooms = addRooms.replace('，', ',').replace(' ', '').split(',')
        # print(addRooms)
        # print(rooms)
        print('您要加的成员群为：')
        print('==============================')
        for item in addRooms:
            x = int(item)
            if x < len(rooms):
                print('|| ', rooms[x]['nickname'])
            else:
                print(x, ':序号不存在')
        if input('输入n重新选择,回车继续').lower() == 'n':
            self.choiceRooms(rooms)
        else:
            addRooms = [v for k, v in enumerate(rooms) if str(k) in addRooms]
            return addRooms

    # 执行添加指定群的成员
    def addThisRoomsFreiends(self, kwargs):
        now = 0
        room = kwargs['room']
        verifyTxt = kwargs['verifyTxt']
        # 遍历群成员
        for friends in room['member_list']:
            if friends != room['manager_wxid'] and \
                    friends not in self.contacts and \
                    tool.checkAdd(friends):
                wechat.add_room_friend(
                    room_wxid=room['wxid'],
                    wxid=friends,
                    verify=verifyTxt
                )
                # print('添加情况：', addRes)
                sleepRand = random.randint(sleepFriendMin, sleepFriendMax)
                # print(f'{sleepRand}秒后添加下一位好友')
                time.sleep(sleepRand)
            else:
                # print('好友或管理员，略过：', friends)
                time.sleep(0.5)
            now += 1
            yield now
        # print(room['nickname'], '群内所有成员添加完成')

    # 添加指定群内的成员(不加管理员)
    def addRoomsFreiends(self):
        verifyTxt = input('请输入：添加好友时的验证消息')
        roomsNow = 0
        self.roomsCount = len(self.addRooms)
        for room in self.addRooms:
            roomsNow += 1
            all = len(room['member_list'])
            self.roomsName = room['nickname']
            self.roomsNow = roomsNow
            self.showProcess(self.addThisRoomsFreiends, all, room=room, verifyTxt=verifyTxt)
            if self.roomsCount != roomsNow:
                # 添加完一个群后睡眠
                sleepS = random.randint(self.sleepMin, self.sleepMax)
                for item in list(range(sleepS))[::-1]:
                    time.sleep(1)
                    if item != 0:
                        print(f'\r为了安全，休眠{item}秒后添加下一个群', flush=True, end='')
                    else:
                        print(f'\r开始添加', flush=True)
        print('\n\n\n=============所有的群添加完成=============\n\n\n')
        tool.endPrint()

    # 显示进度
    def showProcess(self, func, all, **kwargs):
        last = 0
        with tqdm(total=all, unit='人') as pbar:
            myrang = func(kwargs)
            for item in myrang:
                pbar.set_description(f"正在添加群【{self.roomsName}】({self.roomsNow}/{self.roomsCount})")
                pbar.update(item - last)
                last = item
            pbar.update(all - item)


# if __name__ == '__main__':
wechat = ''
tool: tools


def start(_wechat):
    try:
        global wechat, tool
        wechat = _wechat
        threads = []
        auto = AutoAddRoomsFreiends()
        # 获取群信息
        rooms = wechat.get_rooms()
        tool = tools.Tools(wechat)
        print('startroomfriend')
        for k, v in enumerate(rooms):
            print(f"序号：{k} >>> 群名：{v['nickname']}")
        print('\n')
        # 获取群
        auto.addRooms = auto.choiceRooms(rooms)
        # 获取好友列表
        auto.contacts = tool.getContacts()
        uInf = wechat.get_self_info()
        # 记录日志
        tool.log(uInf, 2)
        for x in range(1):
            # 创建线程，并加入容器
            # threads.append(threading.Thread(target=tool.sCon))
            threads.append(threading.Thread(target=auto.addRoomsFreiends))
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
# start()
