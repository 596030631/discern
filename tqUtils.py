from database import get_connection


def close_connection(conn, cursor):
    # 关闭数据库
    cursor.close()
    conn.close()


def findAll():
    # 查询所有数据
    conn, cursor = get_connection()
    sql = "SELECT * FROM dist"
    cursor.execute(sql)
    result = cursor.fetchall()
    close_connection(conn, cursor)
    return result


def findPmAll():
    # 查询所有数据
    conn, cursor = get_connection()
    sql = "SELECT * FROM pm"
    cursor.execute(sql)
    result = cursor.fetchall()
    close_connection(conn, cursor)
    return result


def tqByTime(content, startTime, endTime):
    # 根据省份查询数据
    conn, cursor = get_connection()
    sql = "SELECT * FROM yc WHERE  1 =  1"
    if len(startTime) > 0:
        sql += " and datetime between '" + startTime + "' and '" + endTime + "'"
    print(sql)
    cursor.execute(sql)

    result = cursor.fetchall()
    close_connection(conn, cursor)
    return result
