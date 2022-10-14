# 自动生成手机号自动添加好友
# 读取excel自动添加好友(支持手机号和微信号)
import threading
from sys import argv as sys_argv
import random
from time import sleep
from tqdm import tqdm
import psutil
import pyautogui as pyautogui
from pywinauto import Application, mouse, keyboard
from pyclick import HumanClicker
import pandas as pd
from faker import Faker

import tools


class AutoAddPhone:
    def __init__(self):
        self.hc = HumanClicker()
        self.fk = Faker(locale="zh_CN")
        # 验证消息文字
        self.yzxxwz = '我是.'
        # 标签
        self.sign = '陌生'
        # 随机睡眠时长
        self.sleepMin = 1
        self.sleepMax = 120
        self.procId = 0
        self.phoneType = 1
        self.path = ''

    # 获取微信进程id
    def get_pid(self, processName):
        for proc in psutil.process_iter():
            try:
                if (proc.name() == processName):
                    return proc.pid
            except psutil.NoSuchProcess:
                pass
        return -1

    # 键入内容
    def sendKeys(self, xy, txt):
        # print('移动:', xy)
        self.hc.move(xy, random.random())
        mouse.click('left', xy)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('backspace')
        keyboard.send_keys(txt)

    # 获取元素的指定位置
    def get_element_postion(self, element, xc, yc):
        # 元素坐标
        element_position = element.rectangle()
        left = element_position.left
        top = element_position.top
        right = element_position.right
        bottom = element_position.bottom
        x = int(right - (right - left) / 10 * xc)
        y = int(bottom - (bottom - top) / 10 * yc)
        return x, y

    # 获取主窗口
    def get_body(self):
        procId = self.procId
        phoneType = self.phoneType
        path = self.path
        # 打开微信的快捷键
        pyautogui.hotkey('ctrl', 'alt', 'w')
        # 利用进程ID初始化一下实例
        app = Application(backend='uia').connect(process=procId)
        # print(app.window())
        # 检索微信窗口
        main_Win = app.window(class_name='WeChatMainWndForPC')
        # 打印所有的窗口控件信息
        # main_Win.print_control_identifiers()
        # 自动添加好友
        if phoneType == 1:
            while True:
                phone = self.fk.phone_number()
                try:
                    self.addPhone(main_Win, app, phone)
                except Exception as e:
                    print('错误,略过', e)
                sleep(random.randint(self.sleepMin, self.sleepMax))
        # 通过excel添加好友
        elif phoneType == 2:
            if path.endswith('xlsx') or path.endswith('xls'):
                df = pd.read_excel(path)
                count = len(df)
                i = 0
                with tqdm(total=count, unit='人') as pbar:
                    for phone in df['wxid']:
                        i += 1
                        pbar.set_description(f"正在添加【{phone}】({i}/{count})")
                        pbar.update(1)
                        try:
                            self.addPhone(main_Win, app, phone)
                        except Exception as e:
                            pass
                            # print('错误,略过', e)
                        sleep(random.randint(self.sleepMin, self.sleepMax))
                pbar.update(count - i)
                print('excel所有数据添加完毕')
            else:
                print(
                    """
                      ==================================
                      === 文件格式错误 =================
                      === 请关注公众号:嘿python ========
                      === 发送 好友模板 获取正确格式 === 
                      ==================================             
                      """
                )

            # 判断账号是否存在

    def notExists(self, main_Win):
        notExistsType = {
            '该用户不存在': 'WeUIDialog',
            '查找失败': 'WeUIDialog',
        }
        for k, v in notExistsType.items():
            # 如果用户不存在，关闭窗口，继续下次
            notExists = main_Win.child_window(title=k, class_name=v) \
                .exists(timeout=1)
            if notExists:
                notExists = main_Win.child_window(title=k, class_name=v)
                xy = self.get_element_postion(notExists, 4.8, 2.2)
                self.hc.move(xy, random.random())
                mouse.click('left', xy)
                return True
        return False

    # 执行添加微信
    def addPhone(self, main_Win, app, phone):
        # 如果已经添加过，就不再添加了
        if tool.checkAdd(phone) is False:
            return False
        # 找到搜索框
        searchEdit = main_Win.child_window(title="搜索", control_type="Edit").wrapper_object()
        # 设置搜索框红色
        searchEdit.draw_outline(colour='red')
        # 点击搜索框
        searchEdit.click_input()
        # 清空对话框
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('backspace')

        # 键入内容
        searchEdit.type_keys(phone)
        # 找到【网络查找手机/QQ号】按钮
        try:
            searchEdit = main_Win.child_window(title="网络查找手机/QQ号", control_type="Text").wrapper_object()
        except Exception as e:
            searchEdit = main_Win.child_window(title="网络查找微信号", control_type="Text").wrapper_object()
        sleep(random.randint(self.sleepMin, self.sleepMax))
        searchEdit.draw_outline(colour='red')
        searchEdit.click_input()
        sleep(random.randint(self.sleepMin, self.sleepMax))
        # 如果用户不存在，关闭窗口，继续下次
        if self.notExists(main_Win):
            return False
        # 找到搜索到的好友弹窗
        addFriendWin = app.window(class_name='ContactProfileWnd')
        addFriendWin.draw_outline(colour='red')
        addFriendBtn = (self.get_element_postion(addFriendWin, 1.7, 1.8))
        # print(addFriendBtn)
        self.hc.move(addFriendBtn, random.random())
        mouse.click('left', addFriendBtn)
        sleep(random.randint(self.sleepMin, self.sleepMax))
        # 获取添加窗口
        addFrame = main_Win.window(class_name='WeUIDialog')
        ##################   验证消息    ###########################
        xyYZ = self.get_element_postion(addFrame, 8, 8.5)
        # 输入验证消息
        self.sendKeys(xyYZ, self.yzxxwz)

        ##################   标签    ###########################
        xySign = self.get_element_postion(addFrame, 5, 6)
        # 输入标签
        self.sendKeys(xySign, self.sign)
        # 敲回车
        pyautogui.hotkey('enter')
        # 确定添加按钮
        addDone = addFrame.child_window(title="确定", control_type="Button")
        # 点击添加按钮
        addDone.click_input()


wechat = ''
tool: tools


# if __name__ == '__main__':
def start(_wechat):
    global wechat, tool
    wechat = _wechat
    threads = []

    tool = tools.Tools(wechat)
    # 获取好友列表
    # contacts = tool.getContacts()
    uInf = wechat.get_self_info()
    # 记录日志
    tool.log(uInf, 3)
    auto = AutoAddPhone()
    auto.procId = auto.get_pid("WeChat.exe")
    if (auto.procId == -1):
        print("微信未运行")
        input('输入任意键结束')
    else:
        print(
            '''
            ***********************************************
            *                 载入完成                     *             
            * 程序执行期间，将会占用键盘鼠标，建议电脑空闲时使用  *
            ***********************************************
            '''
        )

        argv = sys_argv
        # 支持传入文件方式添加好友
        if len(argv) > 2:
            print(argv[-1])
            auto.path = argv[-1]
            auto.phoneType = 2
        else:
            auto.path = ''
            auto.phoneType = 1
        for x in range(1):
            # 创建线程，并加入容器
            # threads.append(threading.Thread(target=tool.sCon))
            threads.append(threading.Thread(target=auto.get_body))
        for t in threads:
            # 启动所有线程
            t.start()
        for t in threads:
            # 主线程等待进程池中的所有线程执行完毕，避免成为孤儿进程
            t.join()
        auto.get_body()
