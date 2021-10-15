#!/home/jack/anaconda3/envs/py39/bin/python
# -*- coding: UTF-8 -*-
import telnetlib

import psutil
import re
import json
from config import local_ip, format_size
import requests


class MonitorInfos:
    def __init__(self, apps, dirs=set()):
        self.host_ip = local_ip
        self.cpu_percent = psutil.cpu_percent(interval=10)  # 十秒内cpu平均
        self.memory_available = self.__getMemory()[0]
        self.memory_percent = self.__getMemory()[1]
        self.app_health = self.__getAppHealthDic(apps)
        self.dir_health = self.__getDirsHealth(dirs)

    def __getMemory(self):
        virMemory = psutil.virtual_memory()
        return virMemory.available // format_size, virMemory.percent

    def __getDirsHealth(self, dirs=set()):
        """Return disk I/O statistics for every disk installed on the
            system as a dict of raw tuples."""
        resultDict = dict()
        if (len(dirs) == 0):
            pass
        else:
            for dir in dirs:
                diskInfo = psutil.disk_usage(dir)
                tempDict = dict()
                tempDict['free'] = diskInfo.free // format_size
                tempDict['percent'] = diskInfo.percent
                tempDict['total'] = diskInfo.total // format_size
                tempDict['used'] = diskInfo.used // format_size
                resultDict[dir] = tempDict
                # print(dir)
        return resultDict

    def __getAppHealthDic(self, apps):
        resultDict = dict()
        if len(apps) == 0:
            pass
        else:
            tempApps = set()
            if isinstance(apps, dict):
                for proc in psutil.process_iter():
                    # print('pid:' + str(proc.pid) + ' ,name:' + proc.name() + '------开始查询-------')
                    try:
                        appName = proc.name()
                        if appName != apps['name']:
                            continue
                        # print('cwd:' + str(proc.cwd()))
                        # print('environ:' + str(proc.environ()))
                        envRes = re.findall(apps['keyword'], str(proc.environ()))
                        cwdRes = re.findall(apps['keyword'], str(proc.cwd()))
                        cmdRes = re.findall(apps['keyword'], str(proc.cmdline()))
                        if len(envRes) > 0 or len(cwdRes) > 0 or len(cmdRes) > 0:
                            tempApps.add(apps['keyword'])
                            break
                    except (psutil.AccessDenied, psutil.NoSuchProcess):
                        pass
                if apps['keyword'] in tempApps:
                    resultDict[apps['keyword']] = 1
                else:
                    resultDict[apps['keyword']] = 0
            elif isinstance(apps, list):
                for proc in psutil.process_iter():
                    # print('pid:' + str(proc.pid) + ' ,name:' + proc.name() + '------开始查询-------')
                    try:
                        appName = proc.name()
                        # 遍历数组获取字典
                        for appDict in apps:
                            if len(appDict) == 0:
                                break
                            # print(appDict['name'] + ':' + appDict['keyword'])
                            if appDict['name'] != appName:
                                continue
                            if appDict['keyword'] in tempApps:
                                continue
                            # 根据关键字,模糊匹配环境变量和进程工作路径 cmdline
                            # print('cwd:' + str(proc.cwd()))
                            # print('environ:' + str(proc.environ()))
                            # print('cmdline:' + str(proc.cmdline()))
                            envRes = re.findall(appDict['keyword'], str(proc.environ()))
                            cwdRes = re.findall(appDict['keyword'], str(proc.cwd()))
                            cmdRes = re.findall(appDict['keyword'], str(proc.cmdline()))
                            if len(envRes) > 0 or len(cwdRes) > 0 or len(cmdRes) > 0:
                                tempApps.add(appDict['keyword'])
                        if len(tempApps) == len(apps):
                            break
                    except (psutil.AccessDenied, psutil.NoSuchProcess):
                        pass
                for tmpDict in apps:
                    if tmpDict['keyword'] in tempApps:
                        resultDict[tmpDict['keyword']] = 1
                    else:
                        resultDict[tmpDict['keyword']] = 0
        # 处理http 状态
        for appDict in apps:
            try:
                if appDict['name'] != 'http':
                    continue
                url = 'http://' + appDict['keyword']
                res = requests.get(url=url)
                print(res.status_code)
                if (200 == res.status_code):
                    resultDict[appDict['keyword']] = 1
            except:
                pass

        # 处理telnet 状态
        for appDict in apps:
            try:
                if appDict['name'] != 'telnet':
                    continue
                host, port = str(appDict['keyword']).split(":")
                server = telnetlib.Telnet()
                server.open(host, port)
                resultDict[appDict['keyword']] = 1
            except Exception as e:
                print(e)
                pass

        return resultDict

    # def __getAppHealthDic(self, apps=set()):
    #     resultDict = dict()
    #     if (len(apps) == 0):
    #         pass
    #     else:
    #         tempApps = set()
    #         for pid in reversed(psutil.pids()):
    #             appName = psutil.Process(pid).name()
    #             # print(appName)
    #             if (appName in apps):
    #                 tempApps.add(appName)
    #             if (tempApps == apps):
    #                 break
    #         for app in apps:
    #             if (app in tempApps):
    #                 resultDict[app] = 1
    #             else:
    #                 resultDict[app] = 0
    #     return resultDict

    def __str__(self):
        return "[ip=" + self.host_ip + ", cpu_percent=" + str(self.cpu_percent) + \
               ", memory_available=" + str(self.memory_available) + ", memory_percent=" + str(self.memory_percent) + \
               ", app_health=" + str(self.app_health) + \
               ", dir_health=" + str(self.dir_health) + "]"


if __name__ == "__main__":
    process_names = '[{"name":"python","keyword":"monitor.py"},{"name":"nginx","keyword":"master"},{"name":"http","keyword":"10.200.253.60:8081/bdbs"},{"name":"telnet","keyword":"10.200.253.57:60017"}]'
    apps = json.loads(str(process_names))
    monitorInfos = MonitorInfos(apps, [])
    print(monitorInfos)
    print(monitorInfos.host_ip)
    print(monitorInfos.cpu_percent)
