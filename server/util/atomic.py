from django.db import transaction
from rest_framework.views import APIView
from util.response import JsResponse

# 类视图 (事务,保存点的使用)
class MyView2(APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):

        # 设置事务保存点
        s1 = transaction.savepoint()   # 可以设置多个保存点
        try:

            # 数据库操作。。。
            
        except:

            # 事务回滚 (如果发生异常,就回滚事务)
            transaction.savepoint_rollback(s1)  # 可以回滚到指定的保存点
        
        else:
            # 提交事务 (如果没有异常,就提交事务)
            transaction.savepoint_commit(s1)

        # 返回应答
        return JsResponse('ok')
