import pymysql


def get_connection():
    # 连接数据库
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='root',
                           db='dist',
                           charset='utf8')
    cursor = conn.cursor()
    return conn, cursor