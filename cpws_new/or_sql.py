# -*- coding: utf-8 -*-
import time
import pymysql
import cx_Oracle

def connect_mysql_89():
    try:
        connection = pymysql.connect(
            host='192.168.0.89',
            user='zhangshuhan',
            password='Zsh241021.',
            port=3306,
            database="cpws"
        )
        cur = connection.cursor()
        return connection, cur, int(time.time())
    except Exception as e:
        print('connect_oracle_89:', e)
        time.sleep(2)
        return connect_mysql_89()

def connect_mysql_11():
    try:
        connection = pymysql.connect(
            host='192.168.0.11',
            user='zhangshuhan',
            password='Zsh241113.',
            port=3306,
            database="CXY"
        )
        cur = connection.cursor()
        return connection, cur, int(time.time())
    except Exception as e:
        print('connect_oracle_11:', e)
        time.sleep(2)
        return connect_mysql_11()

def connect_mysql_89_whjy():
    try:
        connection = pymysql.connect(
            host='192.168.0.89',
            user='zhangshuhan',
            password='Zsh241021.',
            port=3306,
            database="whjy"
        )
        cur = connection.cursor()
        return connection, cur, int(time.time())
    except Exception as e:
        print('connect_oracle_89:', e)
        time.sleep(2)
        return connect_mysql_89_whjy()


def mysql_insert(sql, data):
    conn_89, cur_89, t = connect_mysql_89()
    if time.time() - t > 600:
        while True:
            try:
                conn_89.ping()
                t = int(time.time())
                print("ping 检测")
                break
            except Exception as e:
                print('function_oracle:', e.args)
                conn_89, cur_89, t = connect_mysql_89()
            time.sleep(2)
    try:
        cur_89.execute(sql, data)
        conn_89.commit()
    except Exception as e:
        print("sql错误原因是:%s" % e)
        conn_89.rollback()


def mysql_select_whjy():
    conn_89, cur_89, t = connect_mysql_89_whjy()
    md5_keys = []
    if time.time() - t > 600:
        while True:
            try:
                conn_89.ping()
                t = int(time.time())
                print("ping 检测")
                break
            except Exception as e:
                print('function_oracle:', e.args)
                conn_89, cur_89, t = connect_mysql_89_whjy()
            time.sleep(2)
    sql = """select * from(
select distinct t.`发行人` from whjy.`债券信息披露提示信息_债券信息` t
union
select distinct t.zqr from whjy.`外汇交易_结构化_应付账款` t
) t1 where length(t1.`发行人`) > 21 order by length(t1.`发行人`);"""
    try:
        cur_89.execute(sql)
        results = cur_89.fetchall()
        for row in results:
            if row and len(row) > 0:  # 检查行是否为空且至少包含一个元素
                md5_keys.append(row[0].replace('\n', ''))
        return list(set(md5_keys))
    except Exception as e:
        print("sql错误原因是:%s" % e)

# print(mysql_select_whjy())


def mysql_select():
    conn_89, cur_89, t = connect_mysql_89()
    md5_keys = []
    if time.time() - t > 600:
        while True:
            try:
                conn_89.ping()
                t = int(time.time())
                print("ping 检测")
                break
            except Exception as e:
                print('function_oracle:', e.args)
                conn_89, cur_89, t = connect_mysql_89()
            time.sleep(2)
    sql = """SELECT md5_key FROM cpwsdata"""
    try:
        cur_89.execute(sql)
        results = cur_89.fetchall()
        for row in results:
            if row and len(row) > 0:  # 检查行是否为空且至少包含一个元素
                md5_keys.append(row[0])
        return md5_keys
    except Exception as e:
        print("sql错误原因是:%s" % e)

def mysql_select_11():
    conn_11, cur_11, t = connect_mysql_11()
    md5_keys = []
    if time.time() - t > 600:
        while True:
            try:
                conn_11.ping()
                t = int(time.time())
                print("ping 检测")
                break
            except Exception as e:
                print('function_oracle:', e.args)
                conn_11, cur_11, t = connect_mysql_11()
            time.sleep(2)
    sql = """select distinct t.`债权人名称` from CXY.`全国企业破产重整案件信息网_total` t where length(t.`债权人名称`) > 21"""
    try:
        cur_11.execute(sql)
        results = cur_11.fetchall()
        for row in results:
            md5_keys.append(row[0].replace('\n',''))
        return list(set(md5_keys))
    except Exception as e:
        print("sql错误原因是:%s" % e)
#
# mysql_11 = mysql_select_11()
# print(mysql_11,len(mysql_11))

# l = []
# z = mysql_select()
# if '03963531905b15d56b241aa797278e22' in z:
#     print("存在")
# else:
#     print("不存在")
# ls = list(set(l))
# print("11111",ls,len(ls))

def connect_oracle_13_ZWRZB_NEW():
    try:
        # 配置说明:用户名 密码 ip:端口号/数据库名
        # connection = cx_Oracle.connect("zxy", "zxy", "218.61.32.88:1521/ORCL25")
        connection = cx_Oracle.connect("ZWRZB_NEW", "Smkj123456", "192.168.0.13:1521/orcl13")
        cur = connection.cursor()
        return connection, cur, int(time.time())
    except Exception as e:
        print('connect_oracle_13:', e)
        time.sleep(2)
        return connect_oracle_13_ZWRZB_NEW()


conn_13, cur_13, t_13 = connect_oracle_13_ZWRZB_NEW()


def oracle_many_13(sql, idx):
    global conn_13, cur_13, t_13
    if time.time() - t_13 > 600:
        while True:
            try:
                conn_13.ping()
                t_13 = int(time.time())
                print("ping 检测")
                break
            except Exception as e:
                print('function_oracle:', e.args)
                conn_13, cur_13, t_13 = connect_oracle_13_ZWRZB_NEW()
            time.sleep(2)
    cur_13.execute(sql)
    if idx % 10 == 0 or idx == -1:
        conn_13.commit()


def oracle_select_13(sql):
    global conn_13, cur_13, t_13
    if time.time() - t_13 > 600:
        while True:
            try:
                conn_13.ping()
                t_13 = int(time.time())
                print("ping 检测")
                break
            except Exception as e:
                print('function_oracle:', e.args)
                conn_13, cur_13, t_13 = connect_oracle_13_ZWRZB_NEW()
            time.sleep(2)
    cur_13.execute(sql)
    results = cur_13.fetchall()
    return results


# 运行oracle
def oracle_update_13(sql):
    conn_13, cur_13, t_13 = connect_oracle_13_ZWRZB_NEW()
    conn_13.ping()
    if time.time() - t_13 > 600:
        while True:
            try:
                conn_13.ping()
                t_13 = int(time.time())
                print("ping 检测")
                break
            except Exception as e:
                print('function_oracle:', e.args)
                conn_13, cur_13, t_13 = connect_oracle_13_ZWRZB_NEW()
            time.sleep(2)
    try:
        cur_13.execute(sql)
        conn_13.commit()
        cur_13.close()
        conn_13.close()
    except Exception as e:
        print("发生未知错误: %s", e)


def oracle_select_only_13(sql):
    conn_13, cur_13, t_13 = connect_oracle_13_ZWRZB_NEW()
    if time.time() - t_13 > 600:
        while True:
            try:
                conn_13.ping()
                t_13 = int(time.time())
                print("ping 检测")
                break
            except Exception as e:
                print('function_oracle:', e.args)
                conn_13, cur_13, t_13 = connect_oracle_13_ZWRZB_NEW()
            time.sleep(2)
    cur_13.execute(sql)
    return cur_13
    # results = cur_89.fetchall()
    # return results
