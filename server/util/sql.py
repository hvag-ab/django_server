from django.db import connections
from typing import Optional, Callable, Any, Union, List, Tuple, Dict


def execute_sql(sql: str, *, args: Optional[list] = None, many: bool = True,
                dbname: str = 'default', keep: str = "dict", action='r',
                func: Callable[[dict], Any] = lambda d: d
                ) -> Union[None,
                           List[Any], Tuple[List[str], List[tuple]],
                           Dict[str, Any], Tuple[List[str], tuple]]:
    """
    :param func: 针对每条dict需要做进一步操作 减少多次循环
    :param sql: sql 语句
    :param many: 获取 一条记录 还是 多条记录
    :param action: 查询操作 or 修改操作
    :param dbname: 使用哪一个数据库 默认是default 有可能会配置多个数据库
    :param keep: dict or tuple dict类型结果  tuple表示返回的是tuple（字段名，字段值） 数据量大 dict性能低
    :param args: sql传递的参数 例如 "SELECT foo FROM bar WHERE baz = %s", [baz] 注意sql中多个%s顺序跟args数组顺序一致
    :return: 修改操作返回None 查询操作 返回对应类型
    """
    if keep not in ['dict', 'tuple']:
        raise ValueError(f'keep must be dict or tuple got {keep}')
    if action not in ['r', 'cud']:  # r表示查询 cud表示增改删
        raise ValueError(f'action is r or cud, got {action}')
    with connections[dbname].cursor() as cursor:
        cursor.execute(sql, args)
        if action == 'cud':
            return
        columns = [col[0] for col in cursor.description]
        if many:
            if keep == 'dict':
                return [
                    func(dict(zip(columns, row)))
                    for row in cursor.fetchall()
                ]
            else:
                return columns, cursor.fetchall()
        else:
            if keep == 'dict':
                return dict(zip(columns, cursor.fetchone()))
            else:
                return columns, cursor.fetchone()


