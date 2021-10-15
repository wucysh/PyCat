# -*- coding: utf-8 -*-
import codecs
import logging
import platform
import random
import time

from bs4 import BeautifulSoup
import pdfkit
from selenium import webdriver


"""
搜狗微信搜索
获取结果并保存PDF
wucysh
20200509
"""

WAIT_TIME = 10  # 等待时间


class SougouWechat():
    def __init__(self):
        if platform.system() == 'Windows':
            self.browser = webdriver.Chrome("E:\py_project\chromedriver.exe")
        else:
            self.browser = webdriver.Chrome("/Users/wucysh/Desktop/Tengern/Python/soft/chromedriver")
        self.browser.implicitly_wait(WAIT_TIME)  # seconds
        self.url = 'https://weixin.sogou.com/'

    def open_ydn_main_page(self):
        """
        打开搜狗微信主页
        :return:
        """
        self.browser.maximize_window()
        self.browser.get(self.url)
        self.browser.implicitly_wait(WAIT_TIME)
        time.sleep(random.uniform(0.9, 2))  # 随机时间

    def search_key(self, key):
        """
        搜索关键字
        :param key:
        :return:
        """
        self.browser.find_element_by_id("query").send_keys(key)
        self.browser.find_element_by_class_name("swz").click()
        time.sleep(random.uniform(0.9, 2))  # 随机时间

    def get_article_info_list(self):
        """
        获取文章信息列表
        :return:
        """
        content = self.browser.page_source.encode('utf-8')
        soup = BeautifulSoup(content, features="html.parser")
        soup = soup.body
        table_url_list = soup.find_all(class_="txt-box")
        for tb_tag in table_url_list:
            source_from = tb_tag.find("div").find("a").text
            if '译' in source_from or '诗' in source_from:
                a_tag = tb_tag.find("h3").find("a")
                print(a_tag.text, end='\t')  # 标题
                print(tb_tag.find("p").text, end='\t')  # 简介
                print(tb_tag.find("div").find("a").text, end='\t')  # 来源
                timeArray = time.localtime(int(tb_tag.find("div").find('script').string.split('(')[2].strip(')').strip('\'')))
                otherStyleTime = time.strftime("%Y%m%d", timeArray)
                print(otherStyleTime, end='\t')  # 时间
                print('https://weixin.sogou.com' + a_tag.attrs["href"])  # href
                # pdfkit.from_url('https://weixin.sogou.com' + a_tag.attrs["href"], a_tag.text + '_out.pdf')
                self.parse_url_to_html('https://weixin.sogou.com' + a_tag.attrs["href"], otherStyleTime + '_' + a_tag.text)
        next = self.browser.find_element_by_id('sogou_next')
        if None != next:
            next.click()
            time.sleep(random.uniform(0.9, 2))  # 随机时间
            self.get_article_info_list()

    def parse_url_to_html(self, url, name):
        """
        解析URL，返回HTML内容
        :param url:解析的url
        :param name: 保存的html文件名
        :return: html
        """
        parent_handle = self.browser.current_window_handle
        try:

            time.sleep(random.uniform(0.9, 1.2))
            js = 'window.open("' + url + '");'
            self.browser.execute_script(js)

            # 获取当前窗口句柄集合（列表类型）
            handles = self.browser.window_handles
            child_handle = None
            for handle in handles:
                if handle != parent_handle:
                    child_handle = handle

            self.browser.switch_to.window(child_handle)
            time.sleep(10)
            # 保存body 文本
            content = self.browser.page_source.encode('utf-8')
            soup = BeautifulSoup(content, features="html.parser")
            soup = soup.body
            codecs.open(name + '.txt', 'wb', encoding='utf-8').write(soup.text)

            # self.browser.execute_script('window.print();')
            filename = '1' + ".html"
            with open(filename, "wb") as f:
                f.write(self.browser.page_source.encode("utf-8", "ignore"))
                f.close()
            pdfkit.from_url(filename, name + '.pdf')
            #
            # content = self.browser.page_source.encode('utf-8')
            # soup = BeautifulSoup(content, features="html.parser")
            #
            # html = str(soup.body)
            #
            # self.save_pdf(html, name)

        except Exception as e:
            logging.error("解析错误", exc_info=True)
        finally:
            self.browser.close()  # 关闭当前窗口（搜狗）
            # 切换回主窗口
            self.browser.switch_to.window(parent_handle)


if __name__ == "__main__":
    sougouwechat = SougouWechat()
    sougouwechat.open_ydn_main_page()
    sougouwechat.search_key(u'姚阳春')
    sougouwechat.get_article_info_list()
    # sougouwechat.getRoot()
    # sougouwechat.browser.quit()
