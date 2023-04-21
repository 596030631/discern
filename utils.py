from database import get_connection


def close_connection(conn, cursor):
    # 关闭数据库
    cursor.close()
    conn.close()


def tq():
    sql = "select tq, count(*)  as num from yc group by tq "
    res = query(sql)
    return res


def fl():
    sql = "select fl, count(*)  as num from yc group by fl"
    res = query(sql)
    return res


def query(sql, *args):
    # 查询数据
    conn, cursor = get_connection()
    cursor.execute(sql, args)
    result = cursor.fetchall()
    close_connection(conn, cursor)
    return result


if __name__ == '__main__':
    print("11")
    data = get_pl_hour()
    print(data)
