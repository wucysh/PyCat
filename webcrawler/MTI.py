# coding=utf-8
import requests
import re
from bs4 import BeautifulSoup
import jieba
import jieba.analyse
import time
"""
中国考研网：调剂信息
结巴分词
"""

class MTI:
    def __init__(self):
        self.host = "http://www.chinakaoyan.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        }
        self.no = 10000

    # 判断是否是MTI
    def is_MTI(self, urlstr):
        response = requests.get(self.host + urlstr, headers=self.headers)
        soup = BeautifulSoup(response.text)
        text_list = soup.find_all(class_="w620 f-l")
        isMTI = False
        for div_text in text_list:
            text = re.sub('\n+', '\n', re.sub('\r', '\n', re.sub('\t', '\n', div_text.text)))
            text_cut = jieba.cut(text, cut_all=True)
            # if isMTI==False and (u"文学" in text_cut) :
            #     # print ", ".join(text_cut)
            #     isMTI=True
            if isMTI == False and (u"翻译" in text_cut):
                isMTI = True
            if isMTI == False and (u"英语" in text_cut):
                isMTI = True
            if isMTI == False and (u"外语" in text_cut):
                isMTI = True
            if isMTI == False and (u"外国语" in text_cut):
                isMTI = True
            if isMTI == False and ("MTI" in text_cut):
                isMTI = True
            if isMTI == False and (u"笔译" in text_cut):
                isMTI = True
            if isMTI == False and (u"口译" in text_cut):
                isMTI = True
                # print re.sub('\n+', '\n', re.sub('\r','\n',re.sub('\t','\n',div_text.text)))
        return isMTI

    # 获取table url
    def get_table_url_list(self, pageNo):
        response = requests.get(self.host + "/tiaoji/schoollist/pagenum/" + pageNo + ".shtml", headers=self.headers)
        soup = BeautifulSoup(response.text)
        table_url_list = soup.find_all(class_="info-item font14")
        for tb_tag in table_url_list:
            a_tag = tb_tag.find("a")
            if self.is_MTI(a_tag.attrs["href"]) and time.strptime(tb_tag.find(class_="time").text,
                                                                  "%Y-%m-%d") > time.strptime("2016-01-01", "%Y-%m-%d"):
                self.no = self.no + 1
                print(str(self.no) + " " + tb_tag.find(class_="time").text + "  " + tb_tag.find(class_="school").text + "  " + self.host + a_tag.attrs["href"])

    def get_url_list(self, pages):
        for pageNo in range(1, pages):
            # print pageNo
            self.get_table_url_list(str(pageNo))


if __name__ == "__main__":
    mti = MTI()
    mti.get_url_list(100)
    print("end")
