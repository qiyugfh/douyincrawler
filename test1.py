# coding: utf-8

from appium import webdriver
import time
from functools import reduce


AIM_ID = "kriswu_1106"  # 要分析的抖音号

def init_driver():
    # 初始化配置，设置Desired Capabilities参数
    desired_caps = {
        "platformName": "Android",
        "platformVersion": "5.1",
        "udid": "192.168.186.104:5555",
        "deviceName": "Samsung Galaxy S6",
        "appPackage": "com.ss.android.ugc.aweme",
        "appActivity": "com.ss.android.ugc.aweme.main.MainActivity",
        "unicodeKeyboard": True,
        "resetKeyboard": True,
        "noReset": True,
        "newCommandTimeout": 600
    }
    # 指定Appium Server
    server = 'http://127.0.0.1:4723/wd/hub'
    # 新建一个Session
    driver = webdriver.Remote(server, desired_caps)
    return driver


def move_to_fans(device, short_id):
    # 进入搜索页面搜索抖音号并进入粉丝页面
    device.find_element_by_id("com.ss.android.ugc.aweme:id/au1").click()
    device.find_element_by_id("com.ss.android.ugc.aweme:id/a86").send_keys(short_id)
    device.find_element_by_id("com.ss.android.ugc.aweme:id/d5h").click()
    device.find_elements_by_id("com.ss.android.ugc.aweme:id/cwm")[0].click()
    device.find_element_by_id("com.ss.android.ugc.aweme:id/adf").click()


def fans_cycle(device):
    fans_done = []
    while True:
        elements = device.find_elements_by_id("com.ss.android.ugc.aweme:id/d9x")
        all_fans = [x.text for x in elements]
        if reduce(lambda x, y: x and y, [(x in fans_done) for x in all_fans]) and fans_done:
            print("遍历结束, 将会终止session")
            break
        for element in elements:
            if element.text not in fans_done:
                element.click()
                time.sleep(2)
                device.press_keycode("4")
                time.sleep(2)
                fans_done.append(element.text)
        device.swipe(600, 1600, 600, 900, duration=1000)
        if len(fans_done) > 30:
            fans_done = fans_done[10:]


if __name__ == '__main__':
    driver = init_driver()
    move_to_fans(driver, AIM_ID)
    fans_cycle(driver)
    driver.quit()

