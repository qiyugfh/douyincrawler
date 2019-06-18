# coding: utf-8

import time
import item



'''
appium要做的事情是：
1、连接Genymotion模拟器（或手机）中的抖音app（版本6.6.0）
2、登陆抖音（抖音号Zsdxapp，登陆账号：18061675168/123456, 18901596648/abc123456）
3、搜索关键字，比如“南京工业大学”，得到下面的所有用户账号，点击关注这些账号
4、以后爬虫直接进入个人页，找到关注的所有账号，对这些账号进行爬视频
'''


class AppiumDouyin:
    # 测试账号
    def __init__(self, driver, account = '18901596648', password = 'abc123456'):
        self._driver = driver
        self._account = account
        self._password = password

    def home_page(self):
        tabbars = []
        while True:
            try:
                #主页下方的导航
                tabbars = self._driver.find_elements_by_id('com.ss.android.ugc.aweme:id/cp7')
                if tabbars is not None and len(tabbars) == 5:
                    break
            except Exception as e:
                print("当前页面不是主页面，等待中...")
                time.sleep(10)
        return tabbars


    #在主页中跳转
    def switch_tab(self, index):
        tabbars = self.home_page()
        print('点击主页中导航条的第%d个tab页' % index)
        tabbars[index].click()
        time.sleep(10)


    # 使用账号登陆
    def account_login(self):
        print('判断账户是否已经登陆')
        #在主界面点击“我”，进入'我的主页'
        self.switch_tab(4)
        print('点击主页中的"我"')
        #抖音号
        try:
            el0 = self._driver.find_element_by_id_nowait("com.ss.android.ugc.aweme:id/dcy")
            if el0.text.startswith('抖音号'):
                print('已经登陆')
        except Exception as e:
            print("账号未登陆，即将登陆")
            try:
                #点击密码登陆
                el0 = self._driver.find_element_by_id("com.ss.android.ugc.aweme:id/bpr")
                el0.click()
                time.sleep(2)
                #账号
                el1 = self._driver.find_element_by_id("com.ss.android.ugc.aweme:id/a5x")
                el1.send_keys(self._account)
                time.sleep(2)
                #密码
                el2 = self._driver.find_element_by_id("com.ss.android.ugc.aweme:id/a5w")
                el2.send_keys(self._password)
                time.sleep(5)
                #同意协议
                self._driver.find_element_by_id("com.ss.android.ugc.aweme:id/bz9").click()
                time.sleep(2)
                #登陆
                self._driver.find_element_by_id("com.ss.android.ugc.aweme:id/nh").click()
                time.sleep(60)
            except Exception as e:
                print("账户密码登陆出现异常")
                print(e)
                return False
        return True


    def search_input(self):
        print('即将在首页根据关键搜索用户账号，并关注')
        #在主界面点击“首页”，进入'首页'
        self.switch_tab(0)
        print('点击主页中的"首页"')
        # 点击首页的搜索按钮
        self._driver.tap_point(990, 143)
        self._driver.tap_point(362, 148)


    def search_clear_input(self):
        # 删除搜索框的内容，准备下一次搜索
        try:
            self._driver.find_element_by_id("com.ss.android.ugc.aweme:id/mq").click()
        except Exception as e:
            print("清空搜索框的内容失败")
            print(e)
            return False
        return True


    # 关注根据关键字搜出来的用户
    def follow_user_list(self, keyword):
        try:
            print(("搜索关键字：%s" % keyword))
            # 输入关键字，点击搜索
            self._driver.find_element_by_id("com.ss.android.ugc.aweme:id/a8g").send_keys(keyword)
            self._driver.find_element_by_id("com.ss.android.ugc.aweme:id/d7r").click()
            time.sleep(2)
            # 切换到用户的tab页
            self._driver.tap_point(450, 284)
            time.sleep(15)
            # 点击所有的关注按钮
            els = self._driver.find_elements_by_id("com.ss.android.ugc.aweme:id/n2")
            count = len(els)
            print("获取搜索到的关注按钮个数：%d" % count)
            user_list = item.getInstance().user_list
            print("user_list: %s" % str(user_list))
            if 'user_info' not in user_list or len(user_list) < count:
                print("获取关键字搜索的结果出现异常")
                return False
            #每屏最多展示7个，如果需要更多，可以不停地往上滑动
            item.getInstance().user_list = user_list[:count]
            for el in els:
                if el.text == "关注":
                    el.click()
                    time.sleep(3)
        except Exception as e:
            print("根据关键字搜索用户出现异常")
            print(e)
            return False
        return True


    # 我关注的账号
    def my_follow_user(self):
        print('即将进入我的关注页面')
        self.switch_tab(4)
        print('点击主页中的"我"')
        try:
            print('点击"我"中的"关注"')
            el = self._driver.find_element_by_id('com.ss.android.ugc.aweme:id/adw')
            print('已关注的用户数量为：%s' % el.text)
            el.click()
            time.sleep(10)
            elementIds = []
            while True:
                user_els = self._driver.find_elements_by_id("com.ss.android.ugc.aweme:id/au3")
                print('开始遍历已关注的用户主页')
                for use_el in user_els:
                    #已经点击过的用户主页不再重复点击
                    if use_el.elementId in elementIds:
                        continue
                    elementIds.append(use_el.elementId)
                    use_el.click()
                    time.sleep(3)
                    try:
                        unique_id_el = self._driver.find_element_by_id('com.ss.android.ugc.aweme:id/dcy')
                        unique_id = unique_id_el.text.split(':')[1].strip()
                        yield unique_id
                        self._driver.tap_point(90, 148)
                    except Exception as e:
                        print("进入个人主页面查找抖音号失败")
                        print(e)
                        return False
                    if self._driver.find_element_by_name('暂时没有更多了') is not None:
                        self._driver.swipe_to_up(445, 1728, 445, 839)
                    else:
                        break
            return True
        except Exception as e:
            print("获取我的关注中的用户列表出现异常")
            print(e)
            return False



