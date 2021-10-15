# -*- coding: utf-8 -*-
import logging
import re

import jdbc_connect
"""
-- TDH HIVE 部分分析工作
-- 获取表分区信息
-- 数据处理
"""

def getTablePartitionTypeMytrimInfo():
    """
        获取表分区类型
        :return:
        """
    databaseName = 'DDWUSER'
    db = jdbc_connect.jdbc_connect('org.apache.hive.jdbc.HiveDriver',
                                   ['jdbc:hive2://127.0.0.1:10000/DDWUSER', 'user', 'pwd'],
                                   '/Users/wucysh/Desktop/Tengern/IdeaProjects/EDWCompare/lib/inceptor-sdk-4.7.0.jar', )

    try:
        sql = "SHOW TABLES IN " + databaseName
        # 学生集合
        rs = db.select(sql)
        print(rs)
        break_no = 0
        for line in rs:
            # for line in tables.split('DDWUSER.'):
            line = line.replace('\n', '').strip()
            line = re.sub('  ', ' ', line)

            # print(line[0], end='\t')
            if '' is line:
                continue
            print(line, end='\t')

            # sql = "SHOW CREATE TABLE " + databaseName + "." + line[0]
            sql = "SHOW CREATE TABLE " + databaseName + "." + line
            desc_rs = db.select(sql)
            # print(str(tuple(desc_rs)))
            partitioned_type = 0
            if 'PARTITIONED BY ' in str(tuple(desc_rs)):
                partitioned_type = 1
            if 'PARTITIONED BY RANGE' in str(tuple(desc_rs)):
                partitioned_type = 2
            print(partitioned_type)

            # break_no += 1
            # if break_no == 10:
            #     break
    except BaseException as e:
        logging.exception(e)
    finally:
        db.closedb()
        print("链接已关闭！")


if __name__ == "__main__":
    """
    主函数
    """
    # 获取表分区类型
    getTablePartitionTypeMytrimInfo()
