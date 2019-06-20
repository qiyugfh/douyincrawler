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
    def __init__(self, appium_driver, account = '18901596648', password = 'abc123456'):
        self._appium_driver = appium_driver
        self._account = account
        self._password = password

    def home_page(self):
        tabbars = []
        while True:
            try:
                #主页下方的导航
                tabbars = self._appium_driver.find_elements_by_id('com.ss.android.ugc.aweme:id/cp7')
                print("tabbar tab count: %d" % len(tabbars))
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
            el0 = self._appium_driver.find_element_by_id_nowait("com.ss.android.ugc.aweme:id/dcy")
            if el0.text.startswith('抖音号'):
                print('已经登陆')
        except Exception as e:
            print("账号未登陆，即将登陆")
            try:
                #点击密码登陆
                el0 = self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/bpr")
                el0.click()
                time.sleep(2)
                #账号
                el1 = self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/a5x")
                el1.send_keys(self._account)
                time.sleep(2)
                #密码
                el2 = self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/a5w")
                el2.send_keys(self._password)
                time.sleep(5)
                #同意协议
                self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/bz9").click()
                time.sleep(2)
                #登陆
                self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/nh").click()
                time.sleep(60)
            except Exception as e:
                print("账户密码登陆出现异常, %s" % str(e))
                return False
        return True


    def search_input(self):
        print('即将在首页根据关键搜索用户账号，并关注')
        #在主界面点击“首页”，进入'首页'
        self.switch_tab(0)
        print('点击主页中的"首页"')
        # 点击首页的搜索按钮
        self._appium_driver.tap(990, 143)
        self._appium_driver.tap(362, 148)


    def search_clear_input(self):
        # 删除搜索框的内容，准备下一次搜索
        try:
            self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/mq").click()
        except Exception as e:
            print("清空搜索框的内容失败, %s" % str(e))
            return False
        return True


    # 关注根据关键字搜出来的用户
    def follow_user_list(self, keyword):
        try:
            print(("搜索关键字：%s" % keyword))
            # 输入关键字，点击搜索
            self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/a8g").send_keys(keyword)
            self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/d7r").click()
            time.sleep(2)
            # 切换到用户的tab页
            self._appium_driver.tap(450, 284)
            time.sleep(15)
            # 点击所有的关注按钮
            els = self._appium_driver.find_elements_by_id("com.ss.android.ugc.aweme:id/n2")
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
            print("根据关键字搜索用户出现异常, %s" % str(e))
            return False
        return True


    # 我关注的账号
    def my_follow_user(self):
        print('即将进入我的关注页面')
        self.switch_tab(4)
        print('点击主页中的"我"')
        try:
            print('点击"我"中的"关注"')
            el = self._appium_driver.find_element_by_id('com.ss.android.ugc.aweme:id/adw')
            print('已关注的用户数量为：%s' % el.text)
            el.click()
            time.sleep(30)
            ids = []
            while True:
                try:
                    #已关注
                    follow_els = self._appium_driver.find_elements_by_id("com.ss.android.ugc.aweme:id/daj")
                    print("len(follow_els): %d" % len(follow_els))
                    user_els = follow_els[:7]
                    print('开始访问已关注的用户主页')
                    for use_el in user_els:
                        use_el.click()
                        time.sleep(10)
                        try:
                            unique_id_el = self._appium_driver.find_element_by_id('com.ss.android.ugc.aweme:id/dcy')
                            print("unique text: %s" % unique_id_el.text)
                            unique_id = unique_id_el.text.split(':')[1].strip()
                            if unique_id in ids:
                                continue
                            ids.append(unique_id)
                            print("ids: %s" % ids)
                            nickname_el = self._appium_driver.find_element_by_id('com.ss.android.ugc.aweme:id/bka')
                            print("正在爬取的用户昵称: %s, 抖音号: %s" % (nickname_el.text, unique_id))
                            yield unique_id
                            while unique_id_el is not None:
                                self._appium_driver.tap(100, 148)
                                try:
                                    unique_id_el = self._appium_driver.find_element_by_id_nowait('com.ss.android.ugc.aweme:id/dcy')
                                    print("返回关注用户列表页失败")
                                except Exception as e:
                                    unique_id_el = None
                                    print("成功返回到关注用户列表页")
                                    time.sleep(5)
                        except Exception as e:
                            print("进入个人主页面查找抖音号失败, %s" % str(e))
                            return False
                    if self._appium_driver.find_element_by_name('暂时没有更多了') is None:
                        #向上滑动页面
                        self._appium_driver.swipe(470, 1800, 470, 450)
                        time.sleep(15)
                    else:
                        break
                except Exception as e:
                    print("获取关注用户列表失败, %s" % str(e))
                    return False
            print("共爬取用户数: %d" % len(ids))
            return True
        except Exception as e:
            print("获取我关注的用户列表出现异常, %s" % str(e))
            return False



