# coding: utf-8

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time

import logging

logger = logging.getLogger('appiumDouyin')

#连接模拟器或者android手机
class AppiumDriver:

    # 假设模拟器屏幕宽高：1080，1920
    def __init__(self, sw=1080, sh=1920):
        self._sw = sw
        self._sh = sh

        # 初始化配置，设置Desired Capabilities参数
        desired_caps = {
            "platformName": "Android",
            "platformVersion": "5.1",
            # "automationName": "uiautomator2",
            "udid": "192.168.186.104:5555",
            "deviceName": "Samsung Galaxy S6",
            # "udid": "9d5a33ea",
            # "deviceName": "MI 4C",
            "appPackage": "com.ss.android.ugc.aweme",
            "appActivity": "com.ss.android.ugc.aweme.main.MainActivity",
            # 关闭手机软键盘
            "unicodeKeyboard": True,
            "resetKeyboard": True,
            # 启动app时不要清除app里的原有的数据
            "noReset": True,
            "newCommandTimeout": 600
        }
        # 指定Appium Server
        server = 'http://127.0.0.1:4723/wd/hub'
        # 新建一个Session
        self._driver = webdriver.Remote(server, desired_caps)
        #当资源未加载出时,最大等待时间(秒)
        self._driver.implicitly_wait(20)
        logger.info("连接抖音app成功")


    def quit(self):
        if self._driver is not None:
            self._driver.close_app()
            self._driver.quit()
            logger.info("退出此次连接")


    def tap(self, x1, y1):
        logger.info("tap point (%d, %d)" % (x1, y1))
        x0 = self._driver.get_window_size()['width']
        y0 = self._driver.get_window_size()['height']
        x2 = int(x1 * x0 / self._sw)
        y2 = int(y1 * y0 / self._sh)
        self._driver.tap([(x2, y2)], 200)
        time.sleep(5)


    def find_element_by_id(self, id):
        logger.info("find element by id: %s" % id)
        while True:
            try:
               el = self._driver.find_element_by_id(id)
            except Exception as e:
                logger.error("find element by id: %s fail, %s" % (id, str(e)))
                time.sleep(3)
            else:
                return el

    def find_element_by_id_nowait(self, id):
        logger.info("find element no wait by id: %s" % id)
        el = self._driver.find_element_by_id(id)
        return el


    def find_elements_by_id(self, id):
        logger.info("find elements by id: %s" % id)
        els = []
        while True:
            try:
               els = self._driver.find_elements_by_id(id)
            except Exception as e:
                logger.error("find elements by id: %s fail, %s" % (id, str(e)))
                time.sleep(3)
            else:
                return els


    def find_element_by_name(self, name):
        logger.info("find element by name: %s" % name)
        try:
            el = self._driver.find_element_by_name(name)
            return el
        except Exception as e:
            logger.error("find element by name: %s fail, %s" % (name, str(e)))
            return None


    def swipe(self, startx, starty, endx, endy):
        logger.info("swipe point (%d, %d) to point(%d, %d)" % (startx, starty, endx, endy))
        x0 = self._driver.get_window_size()['width']
        y0 = self._driver.get_window_size()['height']
        x1 = int(startx * x0 / self._sw)
        y1 = int(starty * y0 / self._sh)
        x2 = int(endx * x0 / self._sw)
        y2 = int(endy * y0 / self._sh)
        self._driver.swipe(x1, y1, x2, y2, 400)
        time.sleep(5)
