import time

# from seleniumwire import webdriver
from selenium import webdriver
from selenium.webdriver.edge.service import Service

import requests
import datetime
import lib
from fake_useragent import UserAgent

ua = UserAgent()
driver_path = lib.driver_path
ex_path = lib.ex_path


# proxies = lib.proxies


# 初始化 web_driver, 记得开代理
class Driver(object):
    def __init__(self, driver_path=r"D:\Python Projects\Webdriver\msedgedriver.exe", extension_path=None, proxies=None):
        self.driver_path = driver_path
        self.ex_path = extension_path
        self.proxies = proxies
        if not extension_path:
            print('Warning: extension path is empty. Could not bypass the paywall')

    def blank_driver(self, mute=False):
        # 初始化selenium driver
        self.browser_option = webdriver.EdgeOptions()
        self.browser_option.add_experimental_option('excludeSwitches', ['enable-automation'])

        self.browser_option.add_argument('--headless=chrome')
        self.browser_option.add_argument('--disable-gpu')
        self.browser_option.add_argument('--user-agent=' + ua.random)
        self.browser_option.add_experimental_option("detach", True)
        if self.ex_path:
            self.browser_option.add_extension(self.ex_path)
        if self.proxies:
            self.browser_option.add_argument('--proxy-server=' + self.proxies)

        preferences = {
            "webrtc.ip_handling_policy": "disable_non_proxied_udp",
            "webrtc.multiple_routes_enabled": False,
            "webrtc.nonproxied_udp_enabled": False
        }
        self.browser_option.add_experimental_option("prefs", preferences)

        prefs = {'profile.managed_default_content_settings.images': 2}
        self.browser_option.add_experimental_option('prefs', prefs)
        driver = webdriver.Edge(service=Service(driver_path),
                                options=self.browser_option,
                                )
        if not mute:
            print('driver initialized')
        return driver

#
# if __name__ == '__main__':
#     driver = Driver(driver_path).blank_driver()
#
#     driver.get('https://browserleaks.com/ip')
#     # driver.get('http://httpbin.org/ip')
#     # driver.get('http://www.google.com')
#     print(driver.page_source)
#     time.sleep(200)
#     driver.quit()
