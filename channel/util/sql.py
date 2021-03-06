from django.db import connections


def execute_sql(sql: str, many: bool = True, dbname: str = 'default', keep: str = "dict", args: list = None):
    """
    :param sql: sql 语句
    :param many: 获取 一条记录 还是 多条记录
    :param dbname: 使用哪一个数据库 默认是default 有可能会配置多个数据库
    :param keep: dict or list dict类型结果  list表示返回的是tuple（字段名，字段值） 数据量大 dict性能低
    :param args: sql传递的参数 例如 "SELECT foo FROM bar WHERE baz = %s", [baz] 注意sql中多个%s顺序跟args数组顺序一致
    :return: list[dict] or dict or tuple[list,list[tuple]] or tuple[list,tuple]
    """
    if keep not in ['dict', 'list']:
        raise ValueError(f'keep must be dict or list got {keep}')
    with connections[dbname].cursor() as cursor:
        cursor.execute(sql, args)
        columns = [col[0] for col in cursor.description]
        if many:
            if keep == 'dict':
                return [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            else:
                return columns, cursor.fetchall()
        else:
            if keep == 'dict':
                return dict(zip(columns, cursor.fetchone()))
            else:
                return columns, cursor.fetchone()
