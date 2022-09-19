# 自动生成手机号自动添加好友
# 读取excel自动添加好友(支持手机号和微信号)
import random
import time
from time import sleep
import psutil
# 获取进程id
import pyautogui as pyautogui
from pywinauto import Application, mouse, keyboard
from pyclick import HumanClicker
import pandas as pd

hc = HumanClicker()
from faker import Faker

fk = Faker(locale="zh_CN")

# 验证消息文字
yzxxwz = '抱歉打扰了-py自动化测试'
# 标签
sign = '陌生'
# 随机睡眠时长
sleepMin = 1
sleepMax = 3


# 获取微信进程id
def get_pid(processName):
    for proc in psutil.process_iter():
        try:
            if (proc.name() == processName):
                # print(proc.name())
                # print(str(proc.pid))
                return proc.pid
        except psutil.NoSuchProcess:
            pass
    return -1


# 键入内容
def sendKeys(xy, txt):
    print('移动:', xy)
    hc.move(xy, random.random())
    mouse.click('left', xy)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('backspace')
    keyboard.send_keys(txt)


# 获取元素的指定位置
def get_element_postion(element, xc, yc):
    # 元素坐标
    element_position = element.rectangle()
    left = element_position.left
    top = element_position.top
    right = element_position.right
    bottom = element_position.bottom
    x = int(right - (right - left) / 10 * xc)
    y = int(bottom - (bottom - top) / 10 * yc)
    return (x, y)


# 获取主窗口
def get_body(procId, phoneType, path=''):
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
            phone = fk.phone_number()
            try:
                addPhone(main_Win, app, phone)
            except Exception as e:
                print('错误,略过', e)
            time.sleep(random.randint(1, 10))
    # 通过excel添加好友
    elif phoneType == 2:
        df = pd.read_excel(path)
        for phone in df['wxid']:
            print('添加：',phone)
            try:
                addPhone(main_Win, app, phone)
            except Exception as e:
                print('错误,略过', e)
            time.sleep(random.randint(1, 10))
        print('excel每行数据添加完毕')

# 判断账号是否存在
def notExists(main_Win):
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
            xy = get_element_postion(notExists, 4.8, 2.2)
            hc.move(xy, random.random())
            mouse.click('left', xy)
            return True
    return False


# 执行添加微信
def addPhone(main_Win, app, phone):
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
    searchEdit = main_Win.child_window(title="网络查找手机/QQ号", control_type="Text").wrapper_object()
    sleep(random.randint(sleepMin, sleepMax))
    searchEdit.draw_outline(colour='red')
    searchEdit.click_input()
    sleep(random.randint(sleepMin, sleepMax))
    # 如果用户不存在，关闭窗口，继续下次
    if notExists(main_Win):
        return False
    # 找到搜索到的好友弹窗
    addFriendWin = app.window(class_name='ContactProfileWnd')
    addFriendWin.draw_outline(colour='red')
    addFriendBtn = (get_element_postion(addFriendWin, 1.7, 1.8))
    print(addFriendBtn)
    hc.move(addFriendBtn, random.random())
    mouse.click('left', addFriendBtn)
    sleep(0.2)
    # 获取添加窗口
    addFrame = main_Win.window(class_name='WeUIDialog')
    ##################   验证消息    ###########################
    xyYZ = get_element_postion(addFrame, 8, 8.5)
    # 输入验证消息
    sendKeys(xyYZ, yzxxwz)

    ##################   标签    ###########################
    xySign = get_element_postion(addFrame, 5, 6)
    # 输入标签
    sendKeys(xySign, sign)
    # 敲回车
    pyautogui.hotkey('enter')
    # 确定添加按钮
    addDone = addFrame.child_window(title="确定", control_type="Button")
    # 点击添加按钮
    addDone.click_input()


if __name__ == '__main__':
    print(
        '''
          **********************************************
          *                 Welcom                     *             
          *                程序载入中                    *
          **********************************************
        '''
    )
    procId = get_pid("WeChat.exe")
    if (procId == -1):
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
        path = ''
        phoneType = int(input('0:停止,1：自动添加，2：通过指定文件添加'))
        if phoneType == 0:
            print('Bye')
            time.sleep(2)
        elif phoneType == 2:
            path = input('请将excel文件拖入')

        get_body(procId, phoneType, path)
