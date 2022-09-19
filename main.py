import sys
import ntchat
'''
群机器人
私聊机器人(自动回复消息，自动回复关键词消息[例如节日祝福])
加群好友(不加群主)
分析群属性
清理僵尸粉
自动加好友
'''
wechat = ntchat.WeChat()
# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)
# 等待登录
wechat.wait_login()
# 向文件助手发送一条消息
wechat.send_text(to_wxid="filehelper", content="ntchat登陆成功")
# 获取群信息
# rooms = wechat.get_rooms()
# for item in rooms:
#     # print('所有群',item)
#     room_members = wechat.get_room_members(item['wxid'])
#     # print('成员列表：', room_members)
#     for x in room_members['member_list']:
#         print(f"账号：{x['account']},昵称：{x['nickname']}, "
#               f"性别：{x['sex']},国家：{x['country']},省：{x['province']},市：{x['city']}")

add_res = wechat.add_room_friend(room_wxid='44606285552@chatroom',
                                 wxid='wxid_0s3gctqf9wy012',
                                 verify='test'
                                 )
print('添加好友：',add_res)
# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    self_wxid = wechat_instance.get_login_info()["wxid"]
    print('收到消息', message)
    # 判断消息不是自己发的，并回复对方
    # if from_wxid != self_wxid:
    #     wechat_instance.send_text(to_wxid=from_wxid, content=f"自动回复：你发送的消息是: {data['msg']}")


try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
