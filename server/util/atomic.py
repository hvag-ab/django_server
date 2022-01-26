from django.db import transaction
from rest_framework.views import APIView
from util.response import JsResponse

# 类视图 (事务,保存点的使用)
class MyView2(APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):

        # do something ...
	try:
	    with transaction.atomic():
		# 需要回滚的操作 一般是对数据库的多个增删改行为
	        # save
		# update 
	except IntegrityError:
	    handle_exception()

	# do something else ...

#上下文with方式
def funcview(request):
    
    with transaction.atomic():
        # 只要是在 with 语句下方的代码,涉及到数据库操作的流程,在操作数据哭库的时候会自动放到一个事务中
        
        # 设置一个事务保存点
    	sl1 = transaction.savepoint()  # 可以设置多个保存点
	
	try:
 
		数据库操作01
   	 	数据库操作02
   	 	...
    	except:
		# 事务回滚, 如果发生异常,可以回滚到制定的保存点 （容易引发TransactionManagementError 问题就是如果并没有保存 反而提交了回滚行为）
		transaction.savepoint_rollback(sl1)
    	else:
		# 提交事务,如果按照预定的执行,没有异常就提交事务
		# (这一步好像是自动提交的,应该没必要)
		transaction.savepoint_commit(sl1)
    
    	return HttpResponse('ok')
