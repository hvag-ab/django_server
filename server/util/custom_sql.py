# from django.db import connections
# connection = connections['my_db_alias']
from django.db import connection  # 使用默认default数据库


def fetchall_dict(cursor, many=True):
    desc = cursor.description
    if desc is None:
        return {}
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in desc]
    if many:
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    else:
        dict(zip(columns, cursor.fetchone()))


def execute_sql(sql, many=True, *args):
    """
    :param sql: sql语句
    :param many: 返回数组or单条记录
    :param args: 传入变量 防止sql注入 注意变量顺序跟args参数顺序必须一致 数量相等
    :return:
    """
    with connection.cursor() as cursor:
        # cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", ['baz'])#这种形式防止sql注入
        cursor.execute(sql, list(args))
        datas = fetchall_dict(cursor, many)
        return datas



