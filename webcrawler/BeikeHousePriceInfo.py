# -*- coding: utf-8 -*-
import logging
from selenium import webdriver
import sys
import time

"""
贝壳二手房交易信息
"""


class HouseInfo():
    def __init__(self):
        self.mark = ''  # 简介
        self.name = ''  # 小区
        self.roomType = ''  # 户型
        self.roomArea = ''  # 面积
        self.listingPrice = ''  # 挂牌价
        self.dealPrice = ''  # 成交价格
        self.dealCycle = ''  # 成交周期
        self.isOneMonth = ''  # 30天成交标志

    def __str__(self):
        return self.mark + "^|^" + str(self.name) + "^|^" + self.roomType + "^|^" + self.roomArea + "^|^" + self.listingPrice + "^|^" + self.dealPrice + "^|^" + self.dealCycle + "^|^" + self.isOneMonth


class beikeHousePriceInfo():
    def __init__(self):
        self.driver = webdriver.Chrome("/Users/wucysh/Desktop/Tengern/Python/soft/chromedriver")  # 驱动浏览器
        self.driver.implicitly_wait(10)  # seconds
        self.url = 'https://hz.ke.com/chengjiao/pg1p1p2/'

    def login_Parse(self):
        self.driver.get(self.url)
        try:
            print("Auto Login......")
            loginName = self.driver.find_element_by_id("loginNameValue").send_keys([""])
            password = self.driver.find_element_by_id("loginPasswd").send_keys([""])
            regFormbox = self.driver.find_element_by_id("regFormbox")
            regFormbox.click()  # 点击保存密码
            dlBtn = self.driver.find_element_by_xpath('//a[@class="login_btn"]')
            dlBtn.click()  # 点击登录按钮
            url = 'https://'
            self.driver.get(url)
            time.sleep(5)

            fm_info_name = self.driver.find_element_by_xpath('//*[@id="completed"]').text

            time.sleep(5)
            # self.allParse()

        except:
            t, v, tb = sys.exc_info()
            print(t, v)
        finally:
            self.driver.close()  # 关闭当前标签

    def getHtml(self):
        self.driver.get(self.url)
        try:
            print("Job info......")
            time.sleep(5)

            self.parseInfo()  # 解析

        except BaseException as e:
            logging.exception(e)

    def parseInfo(self):
        try:

            house_info_list = self.driver.find_element_by_class_name("listContent").find_elements_by_tag_name("li")
            for house_info in house_info_list:
                houseInfo = HouseInfo()
                for text in str(house_info.text).split("\n"):
                    print(text)
                    if "平米" in text:
                        houseInfo.mark = text.strip().replace("  ", " ")
                        houseInfo.name = houseInfo.mark.split(" ")[0]
                        houseInfo.roomType = houseInfo.mark.split(" ")[1]
                        houseInfo.roomArea = houseInfo.mark.split(" ")[2].strip().replace("平米", '')
                    if "30天内成交" in text and "万" in text:
                        houseInfo.isOneMonth = "1"
                        houseInfo.dealPrice = text[text.find("30天内成交") + 6:].replace("万", "").replace("*", "0")
                    if "挂牌" in text and "周期" in text:
                        houseInfo.listingPrice = text[:text.find("万")].replace("挂牌", "")
                        houseInfo.dealCycle = text[text.find("周期") + 2:].replace("天", "")

                print(houseInfo)

        except BaseException as e:
            logging.exception(e)

    def nextPage(self, pageNum):  # pageNum

        self.url = self.url.replace('pg' + str(pageNum - 1), 'pg' + str(pageNum))
        print(self.url)

    def allParse(self):
        for pageNum in range(1, 2):  # 共39414 条记录 每页20条记录 39414/20
            self.nextPage(pageNum)  # 翻页
            self.getHtml()
        self.driver.close()


if __name__ == "__main__":
    houseParse = beikeHousePriceInfo()
    houseParse.allParse()
