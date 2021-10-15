# -*- coding: utf-8 -*-
import logging
import os
import platform
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

from com.pycat.tools.FileHolder import FileHolder

"""
有道云笔记备份笔记文档(Markdown)
"""

WAIT_TIME = 10  # 等待时间
NOTES_SAVE_PATH = 'E:/py_project/Notes'  # 保存目录


class YouDaoNotes():
    def __init__(self):
        if platform.system() == 'Windows':
            self.browser = webdriver.Chrome("E:\py_project\chromedriver.exe")
        else:
            self.browser = webdriver.Chrome("/Users/wucysh/Desktop/Tengern/Python/soft/chromedriver")
        self.browser.implicitly_wait(WAIT_TIME)  # seconds
        self.url = 'https://note.youdao.com/web/#/file/recent/markdown/WEBd469718ac644042b26edc68d6147a2f5/'

    def get_cookies(self):
        """
            解析获取的cookie 用于登录
        :return:
        """
        cookiestr = """ 
                        {'domain': '.youdao.com', 'expiry': 2494249058.422083, 'httpOnly': False, 'name': 'OUTFOX_SEARCH_USER_ID', 'path': '/', 'secure': True, 'value': '"612147484@10.168.11.11"'}
                    {'domain': '.note.youdao.com', 'expiry': 1580294417, 'httpOnly': False, 'name': 'Hm_lvt_53c97531c41019c3315b44853946c2c9', 'path': '/web/', 'secure': False, 'value': '1548169070'}
                    {'domain': '.note.youdao.com', 'expiry': 1555945068.192352, 'httpOnly': True, 'name': 'YNOTE_PERS', 'path': '/', 'secure': True, 'value': 'v2|cqq||YNOTE||web||7776000000||1548169068024||101.245.245.182||qqD45C593515C0660698ADBB00C99BF5A4||QL0f6u6Lpz0Jz0fzWhMYMRqunfgZhfTL0JZ0MUWRLJu0kEPLOGOMgF0PyhHOmOMUG0pK0MQLP4eFRll0Lp4hMOfR'}
                    {'domain': '.note.youdao.com', 'httpOnly': False, 'name': 'Hm_lpvt_53c97531c41019c3315b44853946c2c9', 'path': '/web/', 'secure': False, 'value': '1548758418'}
                    {'domain': '.youdao.com', 'expiry': 1611241058, 'httpOnly': False, 'name': 'OUTFOX_SEARCH_USER_ID_NCOO', 'path': '/', 'secure': True, 'value': '551172216.555068'}
                    {'domain': 'note.youdao.com', 'expiry': 2178894070, 'httpOnly': False, 'name': 'JSESSIONID', 'path': '/', 'secure': True, 'value': 'aaa8dPA4AImzv-X75wYHw'}
                    {'domain': 'note.youdao.com', 'expiry': 1579705057, 'httpOnly': False, 'name': '__yadk_uid', 'path': '/', 'secure': True, 'value': 'QkAm0RPeZphqq9eUqjG4I5evpGOi42ZO'}
                    {'domain': '.note.youdao.com', 'httpOnly': False, 'name': 'YNOTE_CSTK', 'path': '/', 'secure': False, 'value': 'ajOcS6mb'}
                    {'domain': '.youdao.com', 'expiry': 1548758477, 'httpOnly': False, 'name': '_gat', 'path': '/', 'secure': False, 'value': '1'}
                    {'domain': '.youdao.com', 'expiry': 1611830417, 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'GA1.2.1236913433.1548169073'}
                    {'domain': '.note.youdao.com', 'expiry': 2178894070, 'httpOnly': False, 'name': 'YNOTE_LOGIN', 'path': '/', 'secure': True, 'value': '3||1548169068126'}
                    {'domain': '.note.youdao.com', 'expiry': 2178894070, 'httpOnly': True, 'name': 'YNOTE_SESS', 'path': '/', 'secure': True, 'value': 'v2|1j1JHiR_rRlGRLP4kMTuRkEkMYY6LgF0kEhHJF0fwK0zA64UY0fpu0kEhHpSO4zW0zmO4QuRMlMRll0MzEh4Uf0OYOfwBhfYm0'}
                    {'domain': '.youdao.com', 'expiry': 1548844817, 'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False, 'value': 'GA1.2.1698238290.1548742641'}
                    """
        cookies = list()
        for line in cookiestr.strip().split('\n'):
            line = line.strip().replace('\t', '')
            line = eval(line)
            # print(line)
            cookies.append(line)
        return cookies

    def open_ydn_main_page(self):
        """
        通过cookie 登录有道云笔记
        第一次设置等待时间，手动登录获取cookie信息
        :return:
        """
        self.browser.maximize_window()
        self.browser.get(self.url)
        self.browser.implicitly_wait(WAIT_TIME)
        # 设置cookie
        for cookie in self.get_cookies():
            self.browser.add_cookie(cookie)
        self.browser.get(self.url)
        self.browser.implicitly_wait(WAIT_TIME)
        time.sleep(WAIT_TIME)  #
        print('-----打印cookies  共下次登录使用')
        for cookie in self.browser.get_cookies():
            print(cookie)

    def isElementExist(self, element):
        try:
            self.driver.find_element_by_css_selector(element)
            return True
        except:
            return False

    def getRoot(self):
        """
        获取notes 根目录
        :return:
        """
        #  一级目录 我的文件夹
        self.getDirName('', self.browser.find_element_by_tag_name('tree-root'))

    def getDirName(self, path, elem):
        """
            循环获取下级目录
        :param elem:
        :return:
        """
        for li in elem.find_elements_by_tag_name('li'):
            title = li.find_element_by_class_name('file-name').get_attribute('title')
            print(path + '/' + str(title))
            try:
                li.find_element_by_class_name('arrow').click()
                self.getDirName(path + '/' + str(title), li.find_element_by_class_name('tree-container'))
            except:
                pass
            # 获取笔记名称
            self.getDirFileName(path + '/' + str(title), li)

    def getDirFileName(self, path, elem):
        """
            获取目录下的文件名
        :param path:
        :param elem:
        :return:
        """
        try:
            elem.click()
            self.browser.implicitly_wait(WAIT_TIME)
            time.sleep(WAIT_TIME)
            file_view = self.browser.find_element_by_tag_name('file-view')
            for li in file_view.find_elements_by_tag_name('li'):
                title = li.find_element_by_class_name('file-name').find_element_by_tag_name('span').text
                print(path + '/' + str(title))
                self.getNotesInfo(path + '/' + str(title), li)
                # self.browser.switch_to.parent_frame()
                # self.browser.switch_to.default_content()
        except BaseException as e:
            logging.exception(e)
            print("ERROR:" + path)

    def getNotesInfo(self, path, elem):
        """
            笔记信息
        :param path:
        :param elem:
        :return:
        """
        try:
            time.sleep(3)
            elem.click()  # 打开笔记
            # elem.send_keys(Keys.ENTER)  # 打开笔记
            self.browser.implicitly_wait(WAIT_TIME)
            time.sleep(WAIT_TIME)

            iframe = self.browser.find_element_by_class_name('detail-container').find_element_by_tag_name(
                'iframe').get_attribute("id")
            # 打开Markdown 编辑按钮
            if path.strip().endswith('.md'):
                self.browser.find_element_by_css_selector('.file-detail.md').find_element_by_class_name(
                    'hd-btn').click()
            else:
                pass

            time.sleep(WAIT_TIME)

            wait(self.browser, 60).until(EC.frame_to_be_available_and_switch_to_it(iframe))
            # self.browser.switch_to.frame(iframe)

            # self.get_content()

            detail_container = self.browser.find_element_by_tag_name('body')
            # print(detail_container.text)

            if path.strip().endswith('.md'):
                content = detail_container.find_element_by_class_name('ace_content').text
                print(content)
                self.writeMarkDownFile(NOTES_SAVE_PATH + path, content)
            else:
                pass

        except BaseException as e:
            logging.exception(e)
            print("ERROR Note: " + path)
        finally:
            self.browser.switch_to.parent_frame()
            # self.browser.switch_to.default_content()

    def get_content(self):
        """
        BeautifulSoup 进行解析
        :return:
        """
        content = self.browser.page_source.encode('utf-8')
        soup = BeautifulSoup(content, 'lxml')
        soup = soup.body
        print(soup.text)
        return soup

    def writeMarkDownFile(self, path, content):
        """
        写入文件
        :param path:
        :param content:
        :return:
        """
        path = path.strip().strip('/').strip('\\')
        filename = path.split('/')[-1]
        path = os.sep.join(path.split('/')[:-1])
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            #
            FileHolder.writefile(path + os.sep + filename, content)
        except OSError:
            print('makedirs error!!')


if __name__ == "__main__":
    youdaonotes = YouDaoNotes()
    youdaonotes.open_ydn_main_page()
    youdaonotes.getRoot()
    youdaonotes.browser.quit()

    youdaonotes.browser.quit()
