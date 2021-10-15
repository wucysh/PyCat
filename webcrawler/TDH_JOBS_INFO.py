# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from selenium import webdriver
import sys
import time


class JOB():
    def __init__(self):
        self.Job_Id = ''
        self.Description = ''
        self.Submitted = ''
        self.Duration = ''
        self.Stages = ''
        self.Tasks = ''

    def __str__(self):
        return self.Job_Id + "^|^" + str(self.Submitted) + "^|^" + self.Duration + "^|^" + self.Stages + "^|^" + self.Tasks+ "^|^" + self.Description


class TDH_JOBS_INFO():
    def __init__(self):
        self.driver = webdriver.Chrome("/Users/wucysh/Desktop/Tengern/Python/soft/chromedriver")  # 驱动浏览器
        # self.url = 'http://127.0.0.1:44040/jobs/?page=1&items=50&latest=-1'
        self.url = 'http://127.0.0.1:44040/jobs/?page=1&items=50&latest=-1&status=completed'


    def job_Parse(self):
        self.driver.get(self.url)
        try:
            print("Job info......")
            time.sleep(5)

            self.parse_jobs_info()  # 解析jobs信息

        except BaseException as e:
            logging.exception(e)

    def parse_jobs_info(self):
        try:

            jobs_tables = self.driver.find_elements_by_css_selector("table[class=\"table table-bordered table-striped table-condensed sortable\"]")
            for jobs_table in jobs_tables:
                for tr_eles in jobs_table.find_elements_by_tag_name('tr'):
                    job = JOB()

                    # 标题
                    for th_eles in tr_eles.find_elements_by_tag_name('th'):
                        # print(th_eles.text, end='||')
                        # job_info = job_info + "||" + td_eles.text
                        continue
                    i = 0
                    for td_eles in tr_eles.find_elements_by_tag_name('td'):
                        i = i + 1
                        if i == 1:
                            job.Job_Id = td_eles.text
                        if job.Job_Id == '':
                            continue
                        if i == 2:
                            job.Description = td_eles.text
                        if i == 3:
                            # job.Submitted = td_eles.text
                            job.Submitted = datetime.strptime(td_eles.text,'%Y/%m/%d %H:%M:%S')
                        if i == 4:
                            job.Duration = td_eles.text
                        if i == 5:
                            job.Stages = len(td_eles.text.split('/')) > 1 and td_eles.text.split('/')[0] or '0'
                        if i == 6:
                            job.Tasks = len(td_eles.text.split('/')) > 1 and td_eles.text.split('/')[0] or '0'
                    if job.Tasks == '':
                        continue
                    if job.Submitted < datetime.strptime('2017-12-19 19:05:00', '%Y-%m-%d %H:%M:%S') or job.Submitted >datetime.strptime('2017-12-20 00:05:00', '%Y-%m-%d %H:%M:%S'):
                        # print("no:"+job)
                        continue
                    # if int(job.Tasks) > 50:
                    #     print(job)
                    print(job)

        except BaseException as e:
            logging.exception(e)

    def nextPage(self, pageNum):  # pageNum
        # 多次点击
        # self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/ul/li[15]/a').click()  # 翻页

        self.url = self.url.replace('page=' + str(pageNum - 1) + '&', 'page=' + str(pageNum) + '&')
        print(self.url)

    def allParse(self):
        for pageNum in range(1, 12):  # 共39414 条记录 每页20条记录 39414/20
            self.nextPage(pageNum)  # 翻页
            self.job_Parse()
        self.driver.close()


if __name__ == "__main__":
    jobsInfo = TDH_JOBS_INFO()
    # jobsInfo.job_Parse()
    jobsInfo.allParse()

