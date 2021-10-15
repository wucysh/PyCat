# -*-coding:utf-8 -*-
__author__ = 'wucysh'

import os
import threading, time
from datetime import date, timedelta

global nextTime

def execTask():
    subject = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 定时发送测试"
    print(subject)
    os.system('ls -al')


def timerTask():
    global nextTime
    curTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 记录当前时间
    print("当前时间:%s 下次执行时间:%s " % (curTime, nextTime))
    if curTime > nextTime:
        # 重置下次执行
        nextTime = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d") + " 14:30:00"  # 下次执行时间
        # print("下次执行时间:%s" % nextTime)
        execTask()
    # 继续执行
    timer = threading.Timer(5, timerTask)
    timer.start()


if __name__ == "__main__":
    ## 设置启动时间
    nextTime = "2021-07-07 15:00:00"
    timer = threading.Timer(5, timerTask)
    timer.start()
