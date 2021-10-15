# encoding=utf-8
"""
jaydebeapi jdbc 操作工具
"""
import logging

import jaydebeapi


class jdbc_connect:
    """数据库执行操作"""
    # 执行对象
    cursor = ""
    db = False

    # 连接数据库
    def __init__(self, jclassname, driver_args, jars=None, libs=None):
        try:
            # jdbc_connect.db = jaydebeapi.connect(host, username,password, database, charset="utf8")
            # jdbc_connect.db = jaydebeapi.connect('org.apache.hive.jdbc.HiveDriver',
            #                                      ['jdbc:hive2://127.0.0.1:10000/DDWUSER', 'user', 'pwd'],
            #                                      '/Users/wucysh/Desktop/Tengern/IdeaProjects/EDWCompare/lib/inceptor-sdk-4.7.0.jar', )
            jdbc_connect.db = jaydebeapi.connect(jclassname, driver_args, jars, libs)
            jdbc_connect.cursor = self.db.cursor()
        except BaseException:
            print("连接数据库异常")
            self.db.close()

    def select(self, sql):
        """查询数据库 并且返还对象"""
        jdbc_connect.cursor.execute(sql)
        rs = self.cursor.fetchall()
        return rs

    def insert(self, sql):
        """向数据库添加数据
           0成功/1失败
        """
        try:
            jdbc_connect.cursor.execute(sql)
            # jdbc_connect.db.commit()
        except jaydebeapi.DataError:
            jdbc_connect.db.rollback()
            print("执行添加操作失败")
            return "1"
        else:
            return "0"

    def update(self, sql):
        """修改"""
        try:
            jdbc_connect.cursor.execute(sql)
            jdbc_connect.db.commit()
        except jaydebeapi.DataError:
            jdbc_connect.db.rollback()
            print("执行修改操作失败")
            return "1"
        else:
            return "0"

    def delete(self, sql):
        """删除"""
        try:
            jdbc_connect.cursor.execute(sql)
            jdbc_connect.db.commit()
        except jaydebeapi.DataError:
            jdbc_connect.db.rollback()
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

            # import jaydebeapi
            # 
            # conn = jaydebeapi.connect('org.apache.hive.jdbc.HiveDriver',
            #                           ['jdbc:hive2://127.0.0.1:10000/DDWUSER', 'user', 'pwd'],
            #                           '/Users/wucysh/Desktop/Tengern/IdeaProjects/EDWCompare/lib/inceptor-sdk-4.7.0.jar', )
            # 
            # curs = conn.cursor()
            # # curs.execute('CREATE TABLE CUSTOMER'
            # #              '("CUST_ID" INTEGER NOT NULL,'
            # #              ' "NAME" VARCHAR NOT NULL,'
            # #              ' PRIMARY KEY ("CUST_ID"))'
            # #              )
            # # curs.execute("INSERT INTO CUSTOMER VALUES (1, 'John')")
            # curs.execute("SELECT * FROM SYSTEM.DUAL")
            # print(curs.fetchall())
            # 
            # curs.close()
            # 
            # conn.close()

