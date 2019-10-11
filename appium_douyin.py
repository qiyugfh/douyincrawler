# coding: utf-8

import time
import item
import logging


'''
appium要做的事情是：
1、连接Genymotion模拟器（或手机）中的抖音app（版本6.6.0）
2、登陆抖音（抖音号Zsdxapp，登陆账号：18061675168/123456, 18901596648/abc123456）
3、搜索关键字，比如“南京工业大学”，得到下面的所有用户账号，点击关注这些账号
4、以后爬虫直接进入个人页，找到关注的所有账号，对这些账号进行爬视频
'''

logger = logging.getLogger('appiumDouyin')


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
                logger.info("tabbar tab count: %d" % len(tabbars))
                if tabbars is not None and len(tabbars) == 5:
                    break
            except Exception as e:
                logger.warning("当前页面不是主页面，等待中...")
                time.sleep(10)
        return tabbars


    #在主页中跳转
    def switch_tab(self, index):
        tabbars = self.home_page()
        logger.info('点击主页中导航条的第%d个tab页' % index)
        tabbars[index].click()
        time.sleep(10)


    # 使用账号登陆
    def account_login(self):
        logger.info('判断账户是否已经登陆')
        #在主界面点击“我”，进入'我的主页'
        self.switch_tab(4)
        logger.info('点击主页中的"我"')
        #抖音号
        try:
            el0 = self._appium_driver.find_element_by_id_nowait("com.ss.android.ugc.aweme:id/dcy")
            if el0.text.startswith('抖音号'):
                logger.info('已经登陆')
        except Exception as e:
            logger.info("账号未登陆，即将登陆")
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
                logger.error("账户密码登陆出现异常, %s" % str(e))
                return False
        return True


    def search_input(self):
        logger.info('即将在首页根据关键搜索')
        #在主界面点击“首页”，进入'首页'
        self.switch_tab(0)
        logger.info('点击主页中的"首页"')
        # 点击首页的搜索按钮
        self._appium_driver.tap(990, 143)
        self._appium_driver.tap(362, 148)


    def search_clear_input(self):
        # 删除搜索框的内容，准备下一次搜索
        try:
            self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/mq").click()
        except Exception as e:
            logger.error("清空搜索框的内容失败, %s" % str(e))
            return False
        return True


    # 关注根据关键字搜出来的用户
    def follow_user_list(self, keyword):
        try:
            logger.info(("搜索关键字：%s" % keyword))
            # 输入关键字，点击搜索
            self._appium_driver.tap(269, 147)
            self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/a8g").send_keys(keyword)
            self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/d7r").click()
            time.sleep(2)
            # 切换到用户的tab页
            self._appium_driver.tap(450, 284)
            time.sleep(15)
            # 点击所有的关注按钮
            els = self._appium_driver.find_elements_by_id("com.ss.android.ugc.aweme:id/n2")
            count = len(els)
            logger.info("获取搜索到的关注按钮个数：%d" % count)
            user_list = item.getInstance().user_list
            logger.debug("======================user_list: %s" % str(user_list))
            if len(user_list) == 0 or len(user_list) < count:
                logger.info("获取关键字搜索的结果出现异常")
            else:
                #每屏最多展示7个，如果需要更多，可以不停地往上滑动
                item.getInstance().user_list = user_list[:count]
            for el in els:
                if el.text == "关注":
                    el.click()
                    time.sleep(5)
            logger.info("新关注用户数：%d" % count)
        except Exception as e:
            logger.error("根据关键字搜索用户出现异常, %s" % str(e))
            return False
        return True


    # 我关注的账号
    def my_follow_user(self):
        logger.info('即将进入我的关注页面')
        self.switch_tab(4)
        logger.info('点击主页中的"我"')
        try:
            logger.info('点击"我"中的"关注"')
            el = self._appium_driver.find_element_by_id('com.ss.android.ugc.aweme:id/adw')
            logger.info('已关注的用户数量为：%s' % el.text)
            el.click()
            time.sleep(30)
            ids = []
            while True:
                try:
                    follow_els = self._appium_driver.find_elements_by_id("com.ss.android.ugc.aweme:id/db9")
                    logger.info("len(follow_els): %d" % len(follow_els))
                    user_els = follow_els[:7]
                    logger.info('开始访问已关注的用户主页')
                    for use_el in user_els:
                        use_el.click()
                        time.sleep(10)
                        try:
                            unique_id_el = self._appium_driver.find_element_by_id_nowait('com.ss.android.ugc.aweme:id/dcy')
                            logger.info("unique text: %s" % unique_id_el.text)
                            unique_id = unique_id_el.text.split(':')[1].strip()
                            if unique_id in ids:
                                continue
                            ids.append(unique_id)
                            logger.info("ids: %s" % ids)
                            nickname_el = self._appium_driver.find_element_by_id('com.ss.android.ugc.aweme:id/bka')
                            logger.info("正在爬取的用户昵称: %s, 抖音号: %s" % (nickname_el.text, unique_id))
                            yield unique_id
                            while unique_id_el is not None:
                                self._appium_driver.tap(100, 148)
                                try:
                                    unique_id_el = self._appium_driver.find_element_by_id_nowait('com.ss.android.ugc.aweme:id/dcy')
                                    logger.error("返回关注用户列表页失败")
                                except Exception as e:
                                    unique_id_el = None
                                    logger.info("成功返回到关注用户列表页")
                                    time.sleep(5)
                        except Exception as e:
                            logger.error("进入个人主页面查找抖音号失败, %s" % str(e))
                            continue
                    if self._appium_driver.find_element_by_name('暂时没有更多了') is None:
                        #向上滑动页面
                        self._appium_driver.swipe(470, 1800, 470, 450)
                        time.sleep(15)
                    else:
                        break
                except Exception as e:
                    logger.error("获取关注用户列表失败, %s" % str(e))
                    return False
            logger.info("共爬取用户数: %d" % len(ids))
            return True
        except Exception as e:
            logger.error("获取我关注的用户列表出现异常, %s" % str(e))
            return False

    def search_videos(self, keyword):
        try:
            logger.info(("搜索关键字：%s" % keyword))
            # 输入关键字，点击搜索
            self._appium_driver.tap(269, 147)
            self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/a8g").send_keys(keyword)
            self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/d7r").click()
            time.sleep(2)
            # 切换到视频的tab页
            self._appium_driver.tap(294, 286)
            time.sleep(15)
            # 向上翻滚10次，每次返回9个视频
            for i in range(5):
                i = i + 1
                yield i
                # 向上滑动2页面
                self._appium_driver.swipe(470, 1800, 470, 450)
                time.sleep(15)
                self._appium_driver.swipe(470, 1800, 470, 450)
                time.sleep(15)
            self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/mq").click()
        except Exception as e:
            logger.error("根据关键字搜索视频出现异常, %s" % str(e))
            return False
        return True

    def search_videos_by_user_account(self, keyword):
        try:
            logger.info("根据关键字搜索用户账号：%s" % keyword)
            # 输入关键字，点击搜索
            self._appium_driver.tap(269, 147)
            self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/a8g").send_keys(keyword)
            self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/d7r").click()
            time.sleep(2)
            # 切换到用户的tab页
            self._appium_driver.tap(450, 286)
            time.sleep(15)
            # 点击第一个用户
            self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/b2z").click()
            time.sleep(15)
            # 等待爬取用户主页面的视频之后，点击返回
            self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/il").click()
            time.sleep(5)
            # 点击搜索框中的清空
            self._appium_driver.find_element_by_id("com.ss.android.ugc.aweme:id/mq").click()
        except Exception as e:
            logger.error("根据关键字搜索用户视频出现异常, %s" % str(e))
            return False
        return True
