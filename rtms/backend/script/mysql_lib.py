#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:         Rongzhong Xu 80125605
# CreateDate: 2016/11/11

import time
import logging
import mysql.connector
from mysql.connector import errorcode
logger = logging.getLogger('application')


class Mysql(object):

    def __init__(self, host, user, password, name=None, port=3306):
        self.conn_params = {
            "database": name,
            "host": host,
            "user": user,
            "password": password,
            "port": port,
        }
        self.db = None
        self.cursor = None

    def connect(self):
        """
        Connect to Mysql
        """
        try:
            self.db = mysql.connector.connect(**self.conn_params)
            print("connect ok!")
            self.cursor = self.db.cursor(buffered=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
    def execute(self, sqls):
        """
        Execute sql
        """
        try:
            for sql in sqls.split(";"):
                print(sql)
                self.cursor.execute(sql)
            self.db.commit()
        except Exception as err:
            print(err)
            return None

        try:
            rows = self.cursor.fetchall()
        except mysql.connector.errors.InterfaceError:
            return None
        else:
            return rows

    def close(self, ):
        self.db.close()


def mysql_cmd(host, user, password, name=None, port=3306, sqls=""):

    con = Mysql(host, user, password, name, port)
    con.connect()
    result = con.execute(sqls)
    con.close()
    return result



if __name__ == '__main__':
    mysql_cmd('172.30.248.231','mysql','123456',sqls='use ads_contract;delete from ads_contract_schedule where owner_id=114;')

