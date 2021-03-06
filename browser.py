#!/user/bin/python3

import os
import time
import numpy
from selenium import webdriver, common
from PIL import Image
import config
import logging
from util import Util


class TianYanCha:
    __driver = None
    __window = None
    __url = 'https://www.tianyancha.com/'
    __cookie_name = 'tianyancha.cookie'
    __driver_location = Util.get_driver_location()
    __screenshot_dir = Util.get_save_picture_dir()
    __logger = logging.getLogger("TianYanCha")

    # 初始化, 并加载 天眼查根目录
    def __init__(self, window=None):
        self.__driver = webdriver.Chrome(self.__driver_location, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
        self.__driver.maximize_window()
        self.__window = window
        if config.db.get_need_login():
            self.login()

    def login(self):
        self.__logger.info("login")
        cookie = config.db.get_browser_cookie(self.__cookie_name)
        if cookie is not None:
            try:
                self.__driver.get(self.__url)
                for co in cookie:
                    self.__driver.add_cookie(co)
                self.__driver.get(self.__url)
                self.__driver.implicitly_wait(5)
                if self.is_login():
                    return
                else:
                    self.login_get_cookie()
            except EOFError:
                self.login_get_cookie()
        else:
            self.login_get_cookie()

    def login_get_cookie(self):
        # 没有登录成功
        # 我在开发的时候， 刚好在双十一， 一进入该页面， 会弹出一个促销dialog， 故需要close
        self.__driver.get(self.__url)
        self.__driver.implicitly_wait(5)
        try:
            self.__driver.find_element_by_css_selector('.modal-close').click()
        except (common.exceptions.NoSuchElementException, common.exceptions.ElementNotInteractableException,
                common.exceptions.ElementNotInteractableException):
            print("no ad dialog")
        # 点击登录
        self.__driver.find_element_by_css_selector("[onclick='header.loginLink(event)']").click()
        # 循环直到登录成功
        while True:
            try:
                self.__driver.find_element_by_css_selector('.scan-title').text != '手机扫码登录'
            except (common.exceptions.NoSuchElementException,
                    common.exceptions.ElementNotInteractableException,
                    common.exceptions.ElementNotInteractableException,
                    common.exceptions.StaleElementReferenceException
                    ):
                break
            time.sleep(1)
            # print("请扫码登录")
            self.__window.write_event_value('-run-state-', "请扫码登录")
        # 获取了很多个cookie, 类似这样[{'domain':...}, {}, {}]
        # 其实只有一个cookie dict是有效的
        # cookie = {
        #     'domain': 'tianyania.com',
        #     'httpOnly': False,
        #     'path': '/',
        #     'secure': False
        # }
        cookie = self.__driver.get_cookies()
        # 保存cookie
        config.db.save_browser_cookie(self.__cookie_name, cookie)

    def is_login(self):
        try:
            self.__driver.find_element_by_css_selector('.nav-user-name').text
            self.__logger.info('is login')
            return True
        except (common.exceptions.NoSuchElementException, common.exceptions.ElementNotInteractableException,
                common.exceptions.ElementNotInteractableException):
            self.__logger.error('not login')
            return False

    def read_cookie(self, cookie_path):
        return

    def check_and_screenshot(self, company):
        """
        比较company_address和天眼查上地址是否相同， 并截屏，裁剪
        :param pic_root_dir:
        :param company:
        :return:
        """
        ret_company = []
        try:
            company_code = company[0]
            company_name = company[1]
            company_address = company[2]

            self.__driver.get("https://www.tianyancha.com/search?key={value}".format(value=company_name))
            # 获取第一条记录的公司的超链接
            company_url = self.__driver.find_element_by_css_selector(
                ".name,[tyc-event-ch='CompanySearch.Company']").get_attribute('href')
            self.__driver.get(company_url)
            detail_address = self.__driver.find_element_by_css_selector('.detail-content').text
            detail_element = self.__driver.find_element_by_css_selector('.box > .content')
            location = detail_element.location
            size = detail_element.size
            left = location['x']
            top = location['y']
            right = left + size['width'] + config.other_padding
            bottom = top + size['height'] + config.other_padding
            rect = (left, top, right, bottom)
            saved_image_path = "{code}_{name}.png".format(code=company_code, name=company_name)
            # 最终保存的图片路径
            saved_image_path = os.path.join(self.__screenshot_dir, saved_image_path)
            self.__driver.save_screenshot(saved_image_path)
            if config.IS_CROP_IMAGE:
                # 异步截图，提升速度
                config.thread_pool.submit(
                                        self.crop_picture,
                                        saved_image_path, rect
                                        )
            ret_company = numpy.append(company, detail_address)
        except (common.exceptions.NoSuchElementException, common.exceptions.ElementNotInteractableException) as e:
            # 等待5s，方便输入验证码
            time.sleep(5)
            raise e
        finally:
            return ret_company

    def crop_picture(self, image_path, rect):
        self.__logger.info("crop picture")
        try:
            im = Image.open(image_path)
            cropped_image = im.crop(rect)
            cropped_image.save(image_path)
        except OSError as e:
            raise e

    def quit(self):
        # quit Chrome browser
        self.__driver.quit()

    def lazy_click(self, driver,
                   element):  # 简单的封装了一下click方法，页面未加载完成的时候会出现NoSuchElementException或者ElementNotInteractableException错误，捕获错误并重试，默认重试50次，相当于最大等待时长50s
        f = False
        n = 0
        while (not f and n < 50):
            n = n + 1
            try:
                driver.find_element_by_css_selector(element).click()
                f = True
            except (common.exceptions.NoSuchElementException, common.exceptions.ElementNotInteractableException):
                print('lazy-click :页面未加载完成，等待中。')
                time.sleep(1)
                f = False

    def lazy_send(self, driver, element, KeyBords):  # 这里也是等待直到找到元素并成功推送按键命令
        f = False
        n = 0
        while (not f and n < 50):
            n = n + 1
            try:
                driver.find_element_by_css_selector(element).send_keys(KeyBords)
                f = True
            except (common.exceptions.NoSuchElementException, common.exceptions.ElementNotInteractableException,
                    common.exceptions.ElementNotInteractableException):
                print('lazy-send页面未加载完成，等待中。')
                time.sleep(1)
                f = False


class QiChaCha:
    __driver = None
    __window = None
    __url = 'https://www.qcc.com'
    __cookie_name = 'qichacha.cookie'
    __driver_location = Util.get_driver_location()
    __screenshot_dir = Util.get_save_picture_dir()
    __logger = logging.getLogger("QiChaCha")

    # 初始化, 并加载 天眼查根目录
    def __init__(self, window=None):
        self.__driver = webdriver.Chrome(self.__driver_location)
        self.__driver.maximize_window()
        self.__window = window
        if config.db.get_need_login():
            self.login()

    def login(self):
        self.__logger.info("login")
        cookie = config.db.get_browser_cookie(self.__cookie_name)
        if cookie is not None:
            self.__logger.info("QiChaCha cookie exists")
            try:
                self.__driver.get(self.__url)
                for co in cookie:
                    self.__driver.add_cookie(co)
                self.__driver.get(self.__url)
                self.__driver.implicitly_wait(5)
                if self.is_login():
                    return
                else:
                    self.__logger.error("QiChaCha cookie invalid, need re login")
                    self.login_get_cookie()
            except EOFError:
                self.__logger.exception("login by cookie failed")
                self.login_get_cookie()
        else:
            self.__logger.info("QiChaCha cookie not exists")
            self.login_get_cookie()

    def login_get_cookie(self):
        self.__logger.info("login by Scan QR， to Scan QR")
        # 没有登录成功
        # 我在开发的时候， 刚好在双十一， 一进入该页面， 会弹出一个促销dialog， 故需要close
        self.__driver.get(self.__url)
        self.__driver.implicitly_wait(3)
        # 点击登录
        self.__driver.find_element_by_css_selector(".navi-nav .navi-btn").click()
        # 循环直到登录成功
        while True:
            try:
                self.__driver.find_element_by_css_selector('.login-sao-panel .title').text != '扫码登录请使用'
            except (common.exceptions.NoSuchElementException,
                    common.exceptions.ElementNotInteractableException,
                    common.exceptions.ElementNotInteractableException,
                    common.exceptions.StaleElementReferenceException
                    ):
                break
            time.sleep(1)
            self.__window.write_event_value('-run-state-', "请扫码登录")
        # 获取了很多个cookie, 类似这样[{'domain':...}, {}, {}]
        # 其实只有一个cookie dict是有效的
        # cookie = {
        #     'domain': 'tianyania.com',
        #     'httpOnly': False,
        #     'path': '/',
        #     'secure': False
        # }
        cookie = self.__driver.get_cookies()
        config.db.save_browser_cookie(self.__cookie_name, cookie)
        self.__window.write_event_value('-run-state-', "登录成功")
        self.__logger.info("login by Scan QR， after Scan QR， saved cookie")

    def is_login(self):
        try:
            self.__driver.find_element_by_css_selector('.headface')
            return True
        except (common.exceptions.NoSuchElementException, common.exceptions.ElementNotInteractableException,
                common.exceptions.ElementNotInteractableException):
            return False

    def read_cookie(self, cookie_path):
        return

    def check_and_screenshot(self, company):
        """
        比较company_address和天眼查上地址是否相同， 并截屏，裁剪
        :param pic_root_dir:
        :param company:
        :return:
        """
        ret_company = []
        try:
            company_code = company[0]
            company_name = company[1]
            company_address = company[2]

            self.__driver.get("https://www.qcc.com/search?key={value}".format(value=company_name))
            # 获取第一条记录的公司的超链接
            company_url = self.__driver.find_element_by_css_selector(
                ".msearch .frtrt a").get_attribute('href')
            self.__driver.get(company_url)
            detail_address = self.__driver.find_element_by_css_selector(".row .cvlu a[onclick^=showMapModal]").text
            detail_element = self.__driver.find_element_by_css_selector('.row .content')
            location = detail_element.location
            size = detail_element.size
            left = location['x']
            top = location['y']
            right = left + size['width'] + config.other_padding
            bottom = top + size['height'] + config.other_padding
            rect = (left, top, right, bottom)
            saved_image_path = "{code}_{name}.png".format(code=company_code, name=company_name)
            # 最终保存的图片路径
            saved_image_path = os.path.join(self.__screenshot_dir, saved_image_path)
            self.__driver.save_screenshot(saved_image_path)
            if config.IS_CROP_IMAGE:
                # 异步截图，提升速度
                config.thread_pool.submit(
                    self.crop_picture,
                    saved_image_path, rect
                )
            ret_company = numpy.append(company, detail_address)
        except (common.exceptions.NoSuchElementException, common.exceptions.ElementNotInteractableException) as e:
            time.sleep(5)
            raise e
        finally:
            return ret_company

    def crop_picture(self, image_path, rect):
        self.__logger.info("crop picture")
        try:
            im = Image.open(image_path)
            cropped_image = im.crop(rect)
            cropped_image.save(image_path)
        except OSError:
            print(OSError.strerror)

    def quit(self):
        # quit Chrome browser
        self.__driver.quit()

    def lazy_click(self, driver,
                   element):  # 简单的封装了一下click方法，页面未加载完成的时候会出现NoSuchElementException或者ElementNotInteractableException错误，捕获错误并重试，默认重试50次，相当于最大等待时长50s
        f = False
        n = 0
        while (not f and n < 50):
            n = n + 1
            try:
                driver.find_element_by_css_selector(element).click()
                f = True
            except (common.exceptions.NoSuchElementException, common.exceptions.ElementNotInteractableException):
                print('lazy-click :页面未加载完成，等待中。')
                time.sleep(1)
                f = False

    def lazy_send(self, driver, element, KeyBords):  # 这里也是等待直到找到元素并成功推送按键命令
        f = False
        n = 0
        while (not f and n < 50):
            n = n + 1
            try:
                driver.find_element_by_css_selector(element).send_keys(KeyBords)
                f = True
            except (common.exceptions.NoSuchElementException, common.exceptions.ElementNotInteractableException,
                    common.exceptions.ElementNotInteractableException):
                print('lazy-send页面未加载完成，等待中。')
                time.sleep(1)
                f = False
