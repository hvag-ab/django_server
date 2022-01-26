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

#上下文with方式
def funcview(request):
    
    with transaction.atomic():
        # 只要是在 with 语句下方的代码,涉及到数据库操作的流程,在操作数据哭库的时候会自动放到一个事务中
        
        # 设置一个事务保存点
    	sl1 = transaction.savepoint()  # 可以设置多个保存点
 
		数据库操作01
   	 	数据库操作02
   	 	...
    
    	# 事务回滚, 如果发生异常,可以回滚到制定的保存点
    	transaction.savepoint_rollback(sl1)
    
    	# 提交事务,如果按照预定的执行,没有异常就提交事务
    	# (这一步好像是自动提交的,应该没必要)
    	transaction.savepoint_commit(sl1)
    
    	return HttpResponse('ok')
