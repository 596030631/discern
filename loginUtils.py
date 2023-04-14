import pymysql
import hashlib


def get_connection():
    # 连接数据库
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='jianghua521',
                           db='dist',
                           charset='utf8')
    cursor = conn.cursor()
    return conn, cursor


def close_connection(conn, cursor):
    # 关闭数据库
    cursor.close()
    conn.close()


def is_registered(username, email):
    sql = 'select * from user where username=%s or email=%s'
    conn, cursor = get_connection()
    cursor.execute(sql, (username, email))
    result = cursor.fetchone()
    close_connection(conn, cursor)
    if result is None:
        return False
    else:
        return True

# 注册
def register(username, email, password):
    sql = 'insert into user(username, email, password) values(%s, %s, %s)'
    conn, cursor = get_connection()
    cursor.execute(sql, (username, email, password))
    conn.commit()
    close_connection(conn, cursor)
    return True

# 登录
def login(email, password):
    print('----------',email, password)
    sql = 'select * from user where email=%s and password=%s'
    conn, cursor = get_connection()
    cursor.execute(sql, (email, password))
    result = cursor.fetchone()
    close_connection(conn, cursor)
    print(result)
    if result is not None:
        return True
    else:
        return False

# 获取用户名
def getUser(email):
    sql = 'select username from user where email=%s'
    conn, cursor = get_connection()
    cursor.execute(sql, email)
    result = cursor.fetchone()
    close_connection(conn, cursor)
    return result