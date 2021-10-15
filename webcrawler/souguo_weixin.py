# coding=utf-8
import random

import requests
from bs4 import BeautifulSoup
import time
import pdfkit
import logging

"""
搜狗搜索-wechat
"""
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""


class search_wechat:
    def __init__(self):
        self.host = "https://weixin.sogou.com/weixin?query=%E4%BB%BB%E8%AF%9A%E5%88%9A&_sug_type_=&sut=17654&lkt=3%2C1588995790681%2C1588995791016&s_from=input&_sug_=y&type=2&sst0=1588995807100&w=01019900&dr=1"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
        }
        self.cookies = {
            "SUV": "00A91749B4A6930A5B1F307D8BE20171",
            "SUID": "0A93A6B463138B0A5B1A19F1000E4DCB",
            "SUV": "00A91749B4A6930A5B1F307D8BE20171"

        }
        self.no = 10000

    def parse_url_to_html(self, url, name):
        """
        解析URL，返回HTML内容
        :param url:解析的url
        :param name: 保存的html文件名
        :return: html
        """
        try:
            time.sleep(random.uniform(0.9, 1.2))
            response = requests.get(url, headers=self.headers, cookies=self.cookies)
            soup = BeautifulSoup(response.content, features="html.parser")
            # 正文
            body = soup.find(id_="activity-detail")
            html = str(body)

            html = html_template.format(content=html)
            html = html.encode("utf-8")
            self.save_pdf(html, name)
        except Exception as e:
            logging.error("解析错误", exc_info=True)

    def save_pdf(self, htmls, file_name):
        """
        把所有html文件保存到pdf文件
        :param htmls: html文件列表
        :param file_name: pdf文件名
        :return:
        """
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
        pdfkit.from_file(htmls, file_name, options=options)

    # 获取table url
    def get_url_list(self, pageNo):
        """
        解析列表URL
        :param pageNo: 页码
        :return:
        """
        time.sleep(random.uniform(0.9, 3))
        response = requests.get(self.host + "&page=" + pageNo + "&ie=utf8", headers=self.headers, cookies=self.cookies)
        soup = BeautifulSoup(response.text, features="html.parser")
        table_url_list = soup.find_all(class_="txt-box")
        for tb_tag in table_url_list:
            source_from = tb_tag.find("div").find("a").text
            if '译' in source_from or '诗' in source_from:
                a_tag = tb_tag.find("h3").find("a")
                print(a_tag.text, end='\t')  # 标题
                print(tb_tag.find("p").text, end='\t')  # 简介
                print(tb_tag.find("div").find("a").text, end='\t')  # 来源
                timeArray = time.localtime(int(tb_tag.find("div").find('script').string.split('(')[2].strip(')').strip('\'')))
                otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
                print(otherStyleTime, end='\t')  # 时间
                print('https://weixin.sogou.com' + a_tag.attrs["href"])  # href
                # pdfkit.from_url('https://weixin.sogou.com' + a_tag.attrs["href"], a_tag.text + '_out.pdf')
                self.parse_url_to_html('https://weixin.sogou.com' + a_tag.attrs["href"], a_tag.text + '_out.pdf')

    def next_page(self, pages):
        for pageNo in range(1, pages):
            print(pageNo)
            self.get_url_list(str(pageNo))


if __name__ == "__main__":
    swechat = search_wechat()
    swechat.next_page(3)
    print("end")
