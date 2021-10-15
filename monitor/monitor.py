#!/home/jack/anaconda3/envs/py39/bin/python
# -*- coding: UTF-8 -*-
import pymysql
from config import mysql_host, mysql_port, mysql_db, mysql_user, mysql_password
from config import local_ip, default_sleep
import time
from MonitorInfos import MonitorInfos
import logging
import os, json

# logDir = os.getcwd() +'/SystemMonitor/log/'
logDir = os.getcwd() + '/log/'
logFileName = time.strftime('%Y%m%d%H%M') + '_' + local_ip.replace('.', '_') + '.log'
logFile = logDir + logFileName
if not os.path.exists(logDir + logFileName):
    os.chdir(logDir)
    file = open(logFileName, 'w')
    file.close()
logging.basicConfig(filename=logFile, level=logging.INFO,
                    filemode='w',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


# 返回一个元祖(cursor, connection)
def getMySQLInfos():
    conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password,
                           database=mysql_db, port=mysql_port, charset="utf8")
    return conn.cursor(), conn


def run():
    sleep_seconds = default_sleep
    try:
        cursor, conn = getMySQLInfos()
        cursor.execute("select frequency, process_names, dir_names, upchat_ids, cpu_percent_alarm,  \
                        memory_percent_alarm, dir_percent_alarm, ifnull(db_max_size,0) as db_max_size, \
                        db_percent_alarm, restart_app_path, log_collect_path \
                        from sys_monitor_config where host_ip=inet_aton('" + local_ip + "') and activate=1")
        result = cursor.fetchall()
        if (len(result) == 0):  # 没有配置文件，直接终止
            logging.info(local_ip + ":no record in sys_monitor_config table!")
            # time.sleep(default_sleep)
            return
        frequency, process_names, dirs_names, upchat_ids, cpu_percent_alarm, memory_percent_alarm, dir_percent_alarm, \
        db_max_size, db_percent_alarm, restart_app_path, log_collect_path = result[0]
        # apps = set(filter(lambda x: x !="", process_names.split("$")))
        apps = json.loads(str(process_names))
        dirs = set(filter(lambda x: x != "", dirs_names.split("$")))
        monitorInfos = MonitorInfos(apps, dirs)
        # 数据库监控
        if db_max_size > 0 and db_percent_alarm > 0:
            cursor.execute("select CAST( ROUND((sum( data_length )+ sum( index_length ))/ 1024 / 1024 / 1024 ) AS UNSIGNED ) as used_total \
                           from information_schema.tables")
            dbRes = cursor.fetchall()
            used_total = dbRes[0][0]
            db_used_percent = round(used_total / db_max_size * 100)
        else:
            db_used_percent = -1
        alarm_tag = __setAlarmTag(cpu_percent_alarm, memory_percent_alarm, dir_percent_alarm, db_percent_alarm,
                                  db_used_percent, monitorInfos)
        insertSql = "insert into sys_monitor_info(host_ip, cpu_percent, memory_available, memory_percent, app_health, \
                    dir_health, alarm_tag, upchat_ids, db_used_percent) values \
                     (inet_aton(%s), %s, %s, %s, %s, %s, %s, %s, %s) "
        logging.info(
            local_ip + "sql is:" + insertSql + "and record is:" + str(monitorInfos) + ",db_used_percent=" + str(
                db_used_percent))
        cursor.execute(insertSql, (monitorInfos.host_ip, monitorInfos.cpu_percent, monitorInfos.memory_available,
                                   monitorInfos.memory_percent, json.dumps(monitorInfos.app_health),
                                   json.dumps(monitorInfos.dir_health),
                                   alarm_tag, upchat_ids, db_used_percent
                                   ))
        conn.commit()

        # 内存告警时收集日志
        if monitorInfos.memory_percent > memory_percent_alarm:
            if log_collect_path is not None and len(log_collect_path) > 0:
                logging.info('-------------------开始执行收集日志脚本-------------')
                last = find_last(log_collect_path, '/')
                os.chdir(log_collect_path[0:last])
                logging.info('-----收集日志脚本路径：' + os.getcwd())
                v_return_status = os.system('sh ' + log_collect_path)
                logging.info('-----收集日志脚本执行结果：' + str(v_return_status))

        # 调脚本重启应用
        appRes = monitorInfos.app_health
        for key in appRes:
            if appRes[key] == "upjas" and appRes[key] == 0:
                if restart_app_path is not None and len(restart_app_path) > 0:
                    logging.info('-------------------开始执行重启应用脚本-------------')
                    last = find_last(restart_app_path, '/')
                    os.chdir(restart_app_path[0:last])
                    logging.info('-----调重启应用脚本路径：' + os.getcwd())

        sleep_seconds = frequency * 60
    except Exception as e:
        logging.error(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        time.sleep(sleep_seconds)


def find_last(string, x):
    last_position = -1
    while True:
        position = string.find(x, last_position + 1)
        if position == -1:
            return last_position
        last_position = position


def __setAlarmTag(cpu_percent_alarm, memory_percent_alarm, dir_percent_alarm, db_percent_alarm, db_used_percent,
                  monitorInfos):
    if monitorInfos.cpu_percent > cpu_percent_alarm or monitorInfos.memory_percent > memory_percent_alarm or db_used_percent > db_percent_alarm:
        return 1
    dirs = monitorInfos.dir_health
    apps = monitorInfos.app_health
    for dir in dirs:
        if dirs[dir]['percent'] > dir_percent_alarm:
            return 1
    for key in apps:
        if apps[key] == 0:
            return 1
    return 0


if __name__ == "__main__":
    logging.info('MonitorInfo process is running!')
    while (True):
        run()
