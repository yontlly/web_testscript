# -*- coding: utf-8 -*-
"""
@Time : 2022/12/15 11:05
@Auth : tj
@Function : web自动化关键字
"""
import os
import re
import time

import pyautogui
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from pywinauto.keyboard import send_keys

from webtest.relation import get_relations
from common.common.log import logger


class Web:
    def __init__(self, driver=None):
        # 实例变量，浏览器对象
        self.driver: webdriver.Edge = driver
        # 标识浏览器
        self.br = 'ed'
        # 关联的字典
        self.relations = {}

    def openbrowser(self, br: str = ''):
        """
        打开浏览器
        :param br: 浏览器类型：ed=Edge(默认）,ge=Chrome,ie=InternetExplorer,hh=Firefox
        :return:
        """
        if br == 'ed':
            self.driver = webdriver.Edge()
        elif br == 'hh':
            self.driver = webdriver.Firefox()
            self.br = 'hh'
        elif br == 'ge':
            self.driver = webdriver.Chrome()
            self.br = 'ge'
        elif br == 'ie':
            self.driver = webdriver.Ie()
            self.br = 'ie'
        else:
            option = Options()
            option.add_experimental_option('excludeSwitches', ['enable-automation'])
            option.add_argument('--disable-blink-features=AutomationControlled')
            # 关掉保存密码弹窗
            prefs = {}
            prefs['credentials_enable_service'] = False
            prefs['profile.password_manager_enabled'] = False
            option.add_experimental_option('prefs', prefs)
            self.driver = webdriver.Chrome(options=option)

        # 隐试等待
        self.driver.implicitly_wait(10)
        # 最大化
        self.driver.maximize_window()
        return self.driver

    def geturl(self, url: str = ''):
        """
        打开网站
        :param url: 必须是以http/https开头的标注url地址
        """
        self.driver.get(url)

    @get_relations
    def input(self, lo: str = '', value: str = ''):
        """
        找到并在元素上输入值
        :param lo:元素的定位
        :param value:需要输入的值
        """
        # 处理输入数字的情况
        if type(value) != int:
            ele = self.find_ele(lo)
            # 处理是上传文件的情况
            # 处理需要输入的value里面有点. 认为是文件名
            # 上传图片文件：只适用于元素为<input 标签 type="file"。
            if value.__contains__('.png') or value.__contains__('.jpg') or value.__contains__(
                    '.xlsx') or value.__contains__('.docx'):
                value = os.path.abspath('./lib/file/' + value)
                logger.info(value)

            ele.send_keys(value)
        else:
            ele = self.find_ele(lo)
            ele.send_keys(value)

    def click(self, lo: str = ''):
        """
        找到并点击元素
        :param lo: 元素的定位
        """
        ele = self.find_ele(lo)
        if self.br == 'ie':
            self.driver.execute_script('arguments[0].click()', ele)
        else:
            try:
                ele.click()
            except:
                self.driver.execute_script('arguments[0].click()', ele)

    def sleep(self, t: str = ''):
        """
        固定等待
        :param t: 时间，字符串类型的数字
        """
        try:
            t = float(t)
        except:
            t = 2
        finally:
            # 实现等待时间t秒
            time.sleep(t)

    @get_relations
    def select(self, lo: str = '', visible_text: str = ''):
        """
        在下拉框里面，根据可见文本选择
        :param lo: 下拉框的定位元素
        :param visible_text: 如果是数字则select_by_index(按下标获取)字符串则select_by_visible_text（按文本内容获取）
        """
        ele = self.find_ele(lo)
        select = Select(ele)
        try:
            int(visible_text)
            select.select_by_index(visible_text)
        except:
            select.select_by_visible_text(visible_text)

    def find_ele(self, lo: str = ''):
        """
        元素统一定位
        :param lo:定位方式
        :return:定位到的元素，如果没有定位到返回None
        """
        if lo is None or lo == '':
            ele = None
        # xpath,都是以/或者(开头
        elif lo.startswith('/') or lo.startswith('('):
            ele = self.driver.find_element(By.XPATH, lo)

        # 如果是#开头或者.开头或者包含>或. 那么就用css定位
        elif lo.startswith('#') or lo.startswith('.') or lo.__contains__('>'):
            ele = self.driver.find_elements(By.CSS_SELECTOR, lo)

        else:
            ele = self.driver.find_element(By.ID, lo)

        if ele:
            self.driver.execute_script('arguments[0].style.background = "#ff009b"', ele)

        return ele

    def iframe(self, lo: str = ''):
        """"
        切入进iframe
        :param lo: 需要切入的ifrane元素
        """
        frame = self.find_ele(lo)
        self.driver.switch_to.frame(frame)

    def out_iframe(self):
        """
        跳出iframe
        """
        self.driver.switch_to.default_content()

    def clear(self, lo: str = ''):
        """
        清空输入框
        :param lo: 输入框元素位置
        """
        self.find_ele(lo).clear()

    def toggle_title(self, ti: str = ''):
        """
        切换窗口
        :param ti: 如果不传参数，则关闭当前窗口，切换到新窗口
        如果传整数，则按下标（从0开始）切换，如果传字符串，则按title切换
        """
        # 获取窗口标识
        handles = self.driver.window_handles
        # 没有传参数，关闭窗口，切换到新窗口
        if ti == '':
            self.driver.close()
            self.driver.switch_to.window(handles[1])
        else:
            try:
                # 如果传递的是整数，则按下标切换
                ti = int(ti)
                self.driver.switch_to.window(handles[ti])
            except:
                for h in handles:
                    self.driver.switch_to.window(h)
                    if self.driver.title.__contains__(ti):
                        break

    def quit(self):
        """退出程序，并关闭窗口"""
        self.driver.quit()

    def gettext(self, lo: str = '', reg: str = ''):
        """
        获取元素的文本，传了reg则会使用正则提取
        :param lo: 定位的元素
        :param reg: 正则表达试，如果不为空，且正则匹配到内容，则返回正则匹配后的结果，否则返回原始文本
        :return: 返回内容文本
        """
        ele = self.find_ele(lo)
        text = ele.text
        # 进行正则匹配
        if reg:
            reg_text = re.findall(reg, text)[0]
            # 若匹配到内容，则返回
            if reg_text:
                text = reg_text

        return text

    def gettitle(self):
        """
        获取当前窗口的title
        :return:
        """
        title = self.driver.title
        return title

    def getattr(self, lo: str = '', attr: str = ''):
        """
        获取元素的属性
        :param lo:元素的定位
        :param attr:属性
        :return:属性值
        """
        ele = self.find_ele(lo)
        attr = ele.get_attribute(attr)
        return attr

    def getvalue(self, lo: str = '', attr: str = '', v='verify'):
        """
        获取属性值，可以使用关联传给下一个参数
        :param lo: 元素位置
        :param attr  要获取的属性
        :param v  报错到字典的key
        :return: 返回值
        """
        verify = self.getattr(lo, attr)
        self.relations[v] = verify
        return verify

    @get_relations
    def assertcontains(self, exp_value: str = '', act_value: str = ''):
        """
        断言包含:
        :param exp_value:期望值
        :param act_value:实际结果
        """
        if act_value.__contains__(exp_value):
            logger.info('pass')
            logger.info('期望结果为：{0}'.format(exp_value))
            logger.info('实际结果为：{0}'.format(act_value))
            return True
        else:
            logger.info('FAIT')
            logger.info('期望结果为：{0}'.format(exp_value))
            logger.info('实际结果为：{0}'.format(act_value))
            return False

    def moveby(self, lo: str = '', dist: str = ''):
        """
        鼠标滑动的操作
        :param lo: 元素位置
        :param dist: 滑动的距离
        """
        block = self.find_ele(lo)
        action = ActionChains(self.driver)
        # 按住滑块
        action.click_and_hold(block)
        # 先按住滑块拖动dist个像素
        action.move_by_offset(dist, 0)
        # 松开鼠标使操作生效
        action.release().perform()

    def hover(self, lo: str = ''):
        """
        鼠标移动到某个元素上,鼠标悬停操作
        :param lo: 鼠标要移动到的元素
        """
        acc = self.find_ele(lo)
        # 在driver浏览器上面，创建selenium的鼠标操作类对象
        action = ActionChains(self.driver)
        # 把鼠标移动到元素上，perform是使操作生效
        action.move_to_element(acc).perform()

    def scrolltovisible(self, lo: str = ''):
        """
        滚动元素到可见区域，元素跟窗口的下沿对齐
        :param lo: 元素定位
        """
        ele = self.find_ele(lo)
        self.driver.execute_script('arguments[0].scrollIntoView(false);', ele)

    def keyboard(self, action='Enter'):
        """
        模拟键盘操作
        :param action: 操作方法，传Enter回车，传v粘贴
        """
        if action.__contains__('Enter') or action.__contains__('enter'):
            # 模拟回车
            pyautogui.hotkey('Enter')

        elif action.__contains__('v') or action.__contains__('V'):
            # 模拟粘贴
            pyautogui.hotkey('ctrl', 'v')

    def right_click(self, lo: str = ''):
        """
        模拟鼠标右键
        :param lo: 元素定位
        """
        # 模拟鼠标右键
        cl = self.find_ele(lo)
        action = ActionChains(self.driver)
        action.context_click(cl).perform()

    def send_file(self, file_path):
        """
        file_path : 文件路径
        使用pywinauto库发送文件
        """
        # 输入文件名
        send_keys(file_path)
        time.sleep(3)
        # 输入回车
        send_keys('{VK_RETURN}')
        time.sleep(3)


if __name__ == '__main__':
    web = Web()
    web.openbrowser()
    # 输入地址
    web.geturl('http://10.229.1.237:8282/fed/web-module/')
    web.sleep('2')
    # 点击服务器设置
    web.click('//div[@class="login-setip"]/span')
    # 清空服务器输入框
    web.clear('//input[@class="web-logo-ip"]')
    # 输入服务器地址
    web.input('//input[@class="web-logo-ip"]', '10.229.1.237:8282')
    # 点击确定
    web.click('//span[text()="确定"]')
    # 清空账号输入框
    web.clear('//input[@name="name"]')
    # 输入账号
    web.input('//input[@name="name"]', 'yun02')
    # 输入密码
    web.input('//input[@name="password"]', 'Abc123456')
    # 点击确定
    web.click('//button[@type="submit"]')

    web.sleep('10')

    # 发消息
    # 搜索联系人
    web.click('//input[@class="search-input"]')
    web.input('//input[@class="search-input"]', '运03')
    #
    web.sleep('3')
    # 选择联系人
    web.click('//div[@class="title-box"]')
    web.sleep('3')
    # 输入内容
    web.input('//textarea[@class="fe-textarea"]', '你真好看哈哈')
    # 回车
    web.keyboard()
    web.sleep('4')

    # 撤回
    # # 输入内容
    #     # web.input('//textarea[@class="fe-textarea"]', '你真好看额')
    #     # # 回车
    #     # web.keyboard()
    #     # web.sleep('4')
    #
    # # 撤回
    # # 右键
    # web.right_click('//pre[text()="你真好看额"]')
    # web.sleep('1')
    # # 点击撤回
    # web.click('//li[text()="撤回"]')
    # web.sleep('10')

    # # 右键
    # web.right_click('//pre[text()="你真好看哈哈"]')
    # # 点击复制
    # web.click('//li[text()="复制"]')
    # # 点击输入框
    # web.click('//textarea[@class="fe-textarea"]')
    # # 粘贴
    # web.keyboard('v')
    # web.sleep('4')
    # # 回车
    # web.keyboard()
    # web.sleep('10')

    # 转发
    # # 右键消息
    # web.right_click('//pre[text()="你真好看哈哈"]')
    # # 点击转发
    # web.click('//li[text()="转发"]')
    # # 搜索联系人
    # web.sleep('2')
    # web.click('//input[@id="male"]')
    # web.input('//input[@id="male"]', '生')
    # # 选择联系人
    # web.sleep('2')
    # web.click('(//i[@class="zy-icon zy-icon-"])[1]')
    # # 点击确定
    # web.sleep('5')
    # web.click('(//div[@class="zy-button--box"])[2]')
    # web.sleep('10')

    # # 引用
    # # 右键消息
    # web.right_click('//pre[text()="你真好看哈哈"]')
    # # 点击引用
    # web.click('//li[text()="引用"]')
    # web.sleep('2')
    # # 输入消息内容
    # web.input('//textarea[@class="fe-textarea"]', '这是自动化引用')
    # web.sleep('2')
    # # 点击发送
    # web.click('//button[text()="发送"]')
    # web.sleep('3')

    # # 强通知
    # # 点击强通知
    # web.click('//li[@title="强通知"]')
    # # 清空消息框
    # web.clear('//div[@class="notice-send-box"]/textarea')
    # # 输入强通知消息
    # web.input('//div[@class="notice-send-box"]/textarea', '自动化强通知')
    # # 点击确定
    # web.click('//span[text()="确定"]')
    # web.sleep('3')

    # # 合并转发
    # # 右键
    # web.right_click('//pre[text()="你真好看哈哈"]')
    # # 点击多选
    # web.click('//li[text()="多选"]')
    # web.sleep('1')
    # # 勾选一条消息
    # web.click('//input[@type="checkbox"]')
    # web.sleep('1')
    # # 点击合并转发
    # web.click('(//span[@class="imt-icon"])[2]')
    # web.sleep('1')
    # # 选择联系人
    # web.click('//input[@id="male"]')
    # web.input('//input[@id="male"]', '运03')
    # web.sleep('3')
    # # 选择联系人
    # web.click('//i[@class="zy-icon zy-icon-"]')
    # # 点击确定
    # web.click('(//div[@class="zy-button--box"])[2]')
    # web.sleep('3')

    # # 收藏
    # # 右键
    # web.right_click('(//pre[text()="你真好看哈哈"])[last()]')
    # # 点击收藏
    # web.click('//li[text()="收藏"]')
    # web.sleep('1')
    # # 点击我的收藏
    # web.click('//a[@title="我的收藏"]')
    # web.sleep('2')
    # # 获取文本值
    # attr = web.gettext('(//pre[text()="你真好看哈哈"])[last()]')
    # print(attr)
    # 关闭弹窗
    # web.click('//i[@type="close"]')

    # 上传文件

    # 上传文件
    web.input('//li[@title="发送文件"]/label/input', '云控.xlsx')
    web.sleep('3')
    web.click('//span[text()="发送(Enter)"]')
    web.sleep('14')

    # 发送表情
    # # 点击表情
    # web.click('//li[@title="表情"]')
    # # 点击微笑
    # web.click('//img[@title="微笑"]')
    # # 点击
    # web.click('//li[@title="表情"]')
    # # 点击财迷
    # web.click('//img[@title="财迷"]')
    # web.sleep('2')
    # # 回车发送
    # web.keyboard()
    # web.sleep('2')

    # 语音会议
    # 发起语音
    # web.click('//li[@title="语音通话"]')
    # #
    # web.sleep('2')
    # # 获取元素的属性值
    # s = web.getvalue('//button[@title="邀请成员"]', 'title', 'title')
    # print(s)
    # web.sleep('2')
    # # 断言
    # # print(web.relations)
    # web.assertcontains('邀请成员1', '{title}')
    # # 关闭弹窗
    # web.sleep('2')
    # web.click('(//li[@class="flex-cc"])[2]')
    # # 确定关闭
    # web.click('(//span[text()="确定"])[last()]')
    # web.sleep('4')

    # # 密码锁
    # # 点击密码锁
    # web.click('//li[@title="开启密码锁保护"]')
    # # 输入密码
    # web.input('//input[@type="password"]', 'a123')
    # # 点击启用
    # web.click('//button[@class="confirm"]')
    # # 输入消息
    # web.input('//textarea[@class="fe-textarea"]', '这是加密消息')
    # web.sleep('1')
    # # 回车发送
    # web.keyboard()
    # web.sleep('2')
    # # 关闭密码锁
    # web.click('//li[@title="关闭密码锁保护"]')
    # web.sleep('2')

    # # 发送名片
    # # 点击发送名片
    # web.click('//li[@title="发送名片"]')
    # # 搜索人员
    # web.input('//input[@id="male"]', '生')
    # # 回车
    # web.keyboard()
    # web.sleep('3')
    # # 勾选人员
    # web.click('//span[contains(@class,"zy-circle")]')
    # web.sleep('2')
    # # 点击确定
    # web.click('//span[text()="确定"]')
    # web.sleep('3')

    # # 群聊
    # # 创建群聊
    # # 点击添加
    # web.click('(//a[@title="添加"])[1]/div')
    # web.sleep('2')
    # # 点击创建群聊
    # web.click('//ul[@class="zy-menu"]/li[2]/div')
    # web.sleep('2')
    # # 点击搜索框
    # web.click('//input[@id="male"]')
    # # 搜索人员
    # web.input('//input[@id="male"]', '运')
    # web.sleep('2')
    # # 回车
    # web.keyboard()
    # # 等待
    # web.sleep('2')
    # # 勾选人员
    # web.click('(//span[contains(@class,"zy-circle")])[1]')
    # # 勾选人员2
    # web.click('(//span[contains(@class,"zy-circle")])[2]')
    # # 等待
    # web.sleep('2')
    # # 点击确定
    # web.click('//span[text()="确定"]')
    # web.sleep('4')

    # # 修改群名
    # # 点击群设置
    # web.click('//li[@title="群设置"]')
    # web.sleep('2')
    # # 点击编辑
    # web.click('//*[@class="icon svg-bianji"]')
    # # 清空输入框
    # web.clear('(//input[@class="input"])[1]')
    # # 输入群名
    # web.input('(//input[@class="input"])[1]', '自动化测试群')
    # # 点一下保存
    # web.click('//*[@class="icon svg-bianji"]')
    # # 点一下消息输入框
    # web.click('//textarea[@class="fe-textarea"]')
    # # 等待
    # web.sleep('6')

    # # 发送群消息
    # web.input('//textarea[@class="fe-textarea"]', '自动化测试群消息')
    # # 回车
    # web.keyboard()

    # # 群消息置顶
    # # 点击群设置
    # web.click('//li[@title="群设置"]')
    # web.sleep('2')
    # # 点击设置
    # web.click('//div[text()="设置"]')
    # web.sleep('2')
    # # 置顶群消息
    # web.click('(//span[@class="switch-wrap"])[1]')
    # web.sleep('2')

    # 点击群聊
    # web.click('(//div[@class="info-warp"])[1]')
    # web.sleep('1')

    # # 群投票
    # # 点击插件
    # web.click('//li[@title="插件"]/div')
    # web.sleep('1')
    # # 点击投票
    # web.click('//span[@class="plugin-name"]')
    # web.sleep('2')
    # # # 进入from
    # web.iframe('//div[@id="sdk-iframe"]/iframe')
    # # # 点击主题输入框
    # # web.click('//*[@name="voteTheme"]')
    # # 输入投票主题
    # web.input('//*[@name="voteTheme"]', '自动化测试投票主题')
    # web.sleep('2')
    #
    # # 输入选项内容1
    # web.input('//input[@id="van-field-2-input"]', '可乐')
    # # 输入选项内容2
    # web.input('//input[@id="van-field-3-input"]', '雪碧')
    # # 点击添加选项
    # web.click('(//div[contains(@class,"van-cell__title")])[1]')
    # # 输入选项内容3
    # web.sleep('1')
    # web.input('(//input[@class="van-field__control"])[3]', '凉茶')
    # web.sleep('3')
    # # 点击时间
    # web.click('//div[@class="deadline"]')
    # web.sleep('1')
    # # 选择时间
    # web.click('//div[text()="2023年"]')
    # web.click('//div[text()="01月"]')
    # web.click('//div[text()="02日"]')
    # web.click('//div[text()="18时"]')
    # web.click('//div[text()="30分"]')
    # # 点击确定
    # web.click('//button[text()="确认"]')
    # # 点击发布
    # web.click('//span[@class="van-button__text"]')
    # web.sleep('3')
    #
    # # 点击叉叉
    # web.click('//div[@class="close"]/i')
    # web.sleep('8')

    # # 群公告
    # # 点击群公告
    # web.click('//*[@class="icon svg-notice-entry"]')
    # web.sleep('1')
    # # 点击添加
    # web.click('//*[@class="icon svg-notice-create"]')
    # web.sleep('5')
    # # 进入iframe
    # web.iframe('//div[@id="sdk-iframe"]/iframe')
    # # 进入第二层iframe
    # web.iframe('//iframe[@id="element1_ifr"]')
    # # 输入正文
    # web.click('//body[@id="tinymce"]')
    # web.input('//body[@id="tinymce"]', '自动化测试群公告')
    # web.sleep('1')
    # # 跳出iframe
    # web.out_iframe()
    # # 进入iframe
    # web.iframe('//div[@id="sdk-iframe"]/iframe')
    # # 点击发布
    # web.click('//span[text()="发 布"]')
    # web.sleep('5')
    #
    # # 撤回重编辑群公告
    # # 右键
    # web.right_click('(//div[@class="head-title"])[last()]')
    # web.sleep('1')
    # # 点击撤回重编辑
    # web.click('//li[text()="撤回并重编辑"]')
    # # 点击确定
    # web.click('(//span[text()="确定"])[last()]')
    # web.sleep('2')
    # # 进入iframe
    # web.iframe('//div[@id="sdk-iframe"]/iframe')
    # # 进入第二层iframe
    # web.iframe('//iframe[@id="element1_ifr"]')
    # web.input('//body[@id="tinymce"]', '重编辑重编辑')
    # web.sleep('1')
    # # 跳出iframe
    # web.out_iframe()
    # # 进入iframe
    # web.iframe('//div[@id="sdk-iframe"]/iframe')
    # # 点击发布
    # web.click('//span[text()="发 布"]')
    # web.sleep('5')

    # # 删除群成员
    # # 点击群设置
    # web.click('//li[@title="群设置"]')
    # web.sleep('1')
    # # 鼠标悬停
    # web.hover('(//div[@class="member-item-right"])[last()]')
    # web.sleep('1')
    # # 点击删除
    # web.click('(//div[@class="member-item-right"])[last()]/span')
    # web.sleep('1')
    # # 点击确定
    # web.click('(//span[text()="确定"])[last()]')
    # web.sleep('8')
    #
    # # 添加群成员
    # # 点击群设置
    # web.click('//li[@title="群设置"]')
    # # 点击添加群成员
    # web.click('//*[@title="添加群成员"]')
    # web.sleep('3')
    # # 点击搜索框
    # web.click('//input[@id="male"]')
    # # 输入搜索人员
    # web.input('//input[@id="male"]', '运04')
    # # 回车
    # web.keyboard()
    # web.sleep('3')
    # # 勾选添加的人
    # web.click('(//span[contains(@class,"zy-circle")])[1]')
    # web.sleep('1')
    # # 点击确定
    # web.click('(//span[text()="确定"])[last()]')
    # web.sleep('8')

    # # 指定群管
    # # 点击群设置
    # web.click('//li[@title="群设置"]')
    # # 点击设置
    # web.click('//div[text()="设置"]')
    # web.sleep('1')
    #
    # # 点击设置管理员
    # web.click('//span[text()="设置管理员"]')
    # # 勾选人员
    # web.click('(//span[contains(@class,"zy-circle")])[1]')
    # # 点击确定
    # web.click('(//span[text()="确定"])[last()]')
    # web.sleep('8')

    # # 取消群管
    # # 点击群设置
    # web.click('//li[@title="群设置"]')
    # # 点击设置
    # web.click('//div[text()="设置"]')
    # # 点击设置管理员
    # web.click('//span[text()="设置管理员"]')
    # # 点击叉掉群管
    # web.click('(//i[@type="close"])[last()]')
    # # 点击确定
    # web.click('(//span[text()="确定"])[last()]')
    # web.sleep('8')

    # # 添加群群机器人
    # # 点击群设置
    # web.click('//li[@title="群设置"]')
    # # 点击设置
    # web.click('//div[text()="设置"]')
    # web.sleep('1')
    # # 点击群机器人
    # web.click('//div[@class="shutup-item"]')
    # web.sleep('1')
    # # 点击添加机器人
    # web.click('//span[text()="添加机器人"]')
    # # 点击添加
    # web.click('//span[text()="添 加"]')
    # # 叉掉弹框
    # web.click('//*[@data-icon="close"]')
    # # # 点一下消息输入框
    # web.click('//textarea[@class="fe-textarea"]')
    # web.sleep('3')
    #
    # # 移除群机器人
    # # 点击群设置
    # web.click('//li[@title="群设置"]')
    # # 点击设置
    # web.click('//div[text()="设置"]')
    # # 点击群机器人
    # web.click('//div[@class="shutup-item"]')
    # web.sleep('1')
    # # 鼠标悬浮
    # web.hover('//div[@class="bot-content"]')
    # # 点击删除
    # # web.click('//div[@class="bot-content"]/following-sibling::*/*')
    # web.click('//div[@class="bot-content"]/following-sibling::*')
    # # 点击移除
    #
    # web.click('//span[text()="移 除"]')
    # # # 点一下消息输入框
    # web.click('//textarea[@class="fe-textarea"]')
    # web.sleep('8')

    # # 修改入群验证
    # # 点击群设置
    # web.click('//li[@title="群设置"]')
    # # 点击设置
    # web.click('//div[text()="设置"]')
    # # 点击仅管理员邀请新成员
    # web.click('(//input[@type="radio"])[3]')
    # web.sleep('1')
    # # 需要群管理员验证
    # web.click('(//input[@type="radio"])[2]')
    # web.sleep('1')
    # # 点击不限
    # web.click('(//input[@type="radio"])[1]')
    # web.sleep('2')
    # # # 点一下消息输入框
    # web.click('//textarea[@class="fe-textarea"]')
    # web.sleep('4')

    # 消息免打扰开关
    # 打开免打扰开关
    # # 点击群设置
    # web.click('//li[@title="群设置"]')
    # # 点击设置
    # web.click('//div[text()="设置"]')
    # # 打开消息免打扰
    # web.click('(//span[@class="switch-wrap"])[last()]')
    # # # 点一下消息输入框
    # web.click('//textarea[@class="fe-textarea"]')
    # web.sleep('2')
    #
    #
    # 关闭免打扰开关
    # 点击群设置
    # web.click('//li[@title="群设置"]')
    # # 点击设置
    # web.click('//div[text()="设置"]')
    # # 关闭消息免打扰
    # web.click('(//span[@class="switch-wrap switch-wrap-checked"])[last()]')
    # web.sleep('2')
    # # # 点一下消息输入框
    # web.click('//textarea[@class="fe-textarea"]')
    # web.sleep('8')

    # # 指定成员禁言
    # # 点击群设置
    # web.click('//li[@title="群设置"]')
    # # 点击设置
    # web.click('//div[text()="设置"]')
    # # 点击指定成员禁言
    # web.click('(//div[@class="shutup-item"])[last()]/span')
    # web.sleep('2')
    # # 勾选成员
    # web.click('//input[@type="checkbox"]')
    # # 点击确定
    # web.sleep('1')
    # web.click('//span[text()="确 定"]')
    # web.sleep('1')
    # # # 点一下消息输入框
    # web.click('//textarea[@class="fe-textarea"]')
    # web.sleep('3')
    #
    # # 解除禁言
    # # 点击群设置
    # web.click('//li[@title="群设置"]')
    # # 点击设置
    # web.click('//div[text()="设置"]')
    # # 点击指定成员禁言
    # web.click('(//div[@class="shutup-item"])[last()]/span')
    # web.sleep('2')
    # # 叉掉禁言的人员
    # web.click('(//*[@focusable="false"])[5]')
    # # 点击确定
    # web.click('//span[text()="确 定"]')
    # # # 点一下消息输入框
    # web.click('//textarea[@class="fe-textarea"]')
    # web.sleep('3')

    # # 解散群聊
    # # 点击群设置
    # web.click('//li[@title="群设置"]')
    # # 点击设置
    # web.click('//div[text()="设置"]')
    # # 点击解散群聊
    # web.click('//span[text()="解散群聊"]')
    # web.sleep('1')
    # # 确认解散
    # web.click('(//span[text()="确定"])[last()]')
    # web.sleep('8')

    # # 点击设置
    # web.click('//*[@class="icon svg-menu-set"]')
    # # 点击头像
    # web.sleep('2')
    # web.click('(//*[@class="name"])[last()]')
    # # 点击输入框
    # web.sleep('2')
    # #
    # web.click('//*[@class="icon svg-edit"]')
    # web.sleep('2')
    #
    # web.click('//*[@class="icon svg-xiala"]')
    # web.sleep('2')
    # web.click('//*[text()="男"]')
    # web.sleep('2')
    # # 清空
    # web.clear('(//input[@class="body-input"])[2]')
    # web.sleep('2')
    # web.input('(//input[@class="body-input"])[2]','17000000987')
    # web.sleep('2')
    # # 点击保存
    # web.click('//*[@class="icon svg-edit_pressed"]')
    # web.sleep('8')
