#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
MYSQL 数据库操作
python 3 版本
"""
import os

import pymysql
import logging

from com.pycat.tools.FileHolder import FileHolder


class jdbc_connect:
    """
    数据库执行操作
    """
    # 执行对象
    cursor = ""
    db = False

    # 连接数据库
    def __init__(self, host, user, password, database):
        try:
            jdbc_connect.db = pymysql.connect(host=host, user=user, password=password, database=database)
            jdbc_connect.cursor = self.db.cursor()
        except BaseException:
            print("连接数据库异常")
            self.db.close()

    def select(self, sql):
        """查询数据库 并且返还对象"""
        self.cursor.execute(sql)
        rs = self.cursor.fetchall()
        return rs

    def insert(self, sql):
        """向数据库添加数据
           0成功/1失败
        """
        try:
            self.cursor.ping(reconnect=True)
            self.cursor.execute(sql)
            # jdbc_connect.db.commit()
        except pymysql.DataError:
            jdbc_connect.db.rollback()
            print("执行添加操作失败")
            return "1"
        else:
            return "0"

    def update(self, sql):
        """修改"""
        try:
            self.db.ping(reconnect=True)
            self.cursor.execute(sql)
            self.db.commit()
        except pymysql.DataError:
            jdbc_connect.db.rollback()
            print("执行修改操作失败")
            return "1"
        else:
            return "0"

    def delete(self, sql):
        """删除"""
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except pymysql.DataError:
            self.db.rollback()
            print("执行删除操作失败")
            return "1"
        else:
            return "0"

    def closedb(self):
        """关闭数据库连接"""
        try:
            self.cursor.close()
            self.db.close()
        except BaseException as e:
            logging.exception(e)

        # jdbc_connect = jdbc_connect('localhost', 'root', 'root', 'dsms_dev')
        # date = jdbc_connect.select('SELECT VERSION()')
        # print(date)
        # jdbc_connect.closedb()
        # pass


if __name__ == "__main__":
    jdbc_connect = jdbc_connect('localhost', 'root', 'root', 'dsms_dev')

    path = '/Users/wucysh/Desktop/UionPay/数据库/20210202'
    finish_tables = []
    foreign_tables = []
    foreign_references_tables = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.sql' and 'wucysh' not in file:
                print('-----' + file + '---------------------------------------------------------')
                sqls = FileHolder.readfile(path + '/' + file)
                if 'foreign ' in sqls and ' references ' in sqls:
                    foreign_references_table = sqls.split(' references ')[1].split('(')[0].strip()
                    foreign_tables.append(path + '/' + file)
                    foreign_references_table = path + '/dsms_cs_' + foreign_references_table + '.sql'
                    # 排除已经执行过的表
                    if foreign_references_table not in finish_tables:
                        foreign_references_tables.append(foreign_references_table)
                else:
                    finish_tables.append(path + '/' + file)
                    for sql in sqls.split(';\n'):
                        sql = sql.replace('dsms_cs.', '').replace('#{', '#\{').strip()
                        if '' != sql:
                            # print(sql)
                            try:
                                jdbc_connect.update(sql)
                            except BaseException as e:
                                # logging.exception(e)
                                print('执行错误：' + sql)
                                break
            # else:
            #     print('' + file)
    print('--------------------------------------------------------------')
    foreign_references_tables = list(set(foreign_references_tables))
    for foreign_references_table in foreign_references_tables:
        print(foreign_references_table)
        sqls = FileHolder.readfile(foreign_references_table)
        for sql in sqls.split(';\n'):
            sql = sql.replace('dsms_cs.', '').replace('#{', '#\{').strip()
            if '' != sql:
                # print(sql)
                try:
                    jdbc_connect.update(sql)
                except BaseException as e:
                    logging.exception(e)
                    print('执行错误：' + sql)
                    break
    print('--------------------------------------------------------------')
    for foreign_table in foreign_tables:
        print(foreign_table)
        sqls = FileHolder.readfile(foreign_table)
        for sql in sqls.split(';\n'):
            sql = sql.replace('dsms_cs.', '').replace('#{', '#\{').strip()
            if '' != sql:
                # print(sql)
                try:
                    jdbc_connect.update(sql)
                except BaseException as e:
                    logging.exception(e)
                    print('执行错误：' + sql)
                    break

    try:
        jdbc_connect.closedb()
    except BaseException as e:
        logging.exception(e)
