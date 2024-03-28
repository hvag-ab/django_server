from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from rest_framework import generics, filters
from rest_framework.parsers import JSONParser, FormParser, FileUploadParser, MultiPartParser

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions

from rest_framework import status
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from util.file import DataToExcel
from util.version import APIVersioning
from .filter import ClothesFilter
from .models import Clothes
from .serializers import UserInfoSerializer, RegisterSerializer, ClothesSerializer, \
    MyFileSerializer, ExcelSerializer
from util.response import JsResponse
from util.paginations import CustomPagination



# query参数获取 request.query_params
# form json参数获取 request.data
# url参数获取 self.kwargs
# no 序列化 因序列化后响应速度响应会变慢所以在一些对响应速度要求很高的请求上不使用序列化



# api展示
class API(APIView):
    """
    用到那种方式请求 就重写那种方式
    """

    def get(self, request, *args, **kwargs):
        data = request.query_params
        users = User.objects.all()
        serializer = UserInfoSerializer(users, many=True)
        return JsResponse(data=serializer.data, code=True)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = RegisterSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            # 返回的是对象实例 可以用于后续操作
            return JsResponse(data=serializer.data, status=status.HTTP_201_CREATED, code=True)
        else:
            print(serializer.error_messages)
            print(serializer.errors)  # 打印验证错误
            return JsResponse(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST, code=False)

    def put(self, request, *args, **kwargs): # 全部改
        id = request.data.get('id')
        user = User.objects.get(id=id)
        serializer = UserInfoSerializer(user, data=request.data, partial=False, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return JsResponse(serializer.data)
        return JsResponse(msg=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request, *args, **kwargs): # 只改一部分
        id = request.data.get('id')
        user = User.objects.get(id=id)
        serializer = UserInfoSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return JsResponse(serializer.data)
        return JsResponse(msg=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        id = request.data.get('id')
        deleted, _rows_count = User.objects.filter(id=id).delete()
        return JsResponse(status=status.HTTP_204_NO_CONTENT, data={'rows': _rows_count})

"""
注意路径参数 比如/aaa/<int:pk>/ ... 所有的请求方式都要添加
比如以下
class API(APIView):
    def post(self, request, pk, *args, **kwargs):
        pass

"""


class LoginView(APIView):

    def post(self, request, *args, **kwargs):

        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            return JsResponse(code=False, msg="该用户不存在")
        if not user.check_password(password):
            return JsResponse(code=False, msg="密码错误")
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        token = api_settings.JWT_AUTH_HEADER_PREFIX + ' ' + token
        return JsResponse(data=token)


class RegisterView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = RegisterSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            # 返回的是对象实例 可以用于后续操作
            return JsResponse(data=serializer.data, status=status.HTTP_201_CREATED, code=True)
        else:
            print(serializer.error_messages)
            print(serializer.errors)  # 打印验证错误
            return JsResponse(msg=serializer.errors, code=False)


class DetailAPI(generics.RetrieveUpdateDestroyAPIView):  # 可以单独使用DestroyAPIView，RetrieveAPIView
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.AllowAny]

    _ignore_model_permissions = True  # 添加对象层级的权限一定要添加这个属性 否则会运行模型层级的权限，导致失败，缺陷就是没有模型层级的权限

    lookup_url_kwarg = 'pk'  # uri参数   path('user/<int:pk>/', views.DetailAPI.as_view()),

    def get_object(self):
        # url参数
        data = self.kwargs
        # params参数 就是url 里面的参数
        # data = self.kwargs
        obj = get_object_or_404(self.get_queryset(), id=data.get('pk'))
        self.check_object_permissions(self.request, obj)  # 显示调用对象级权限检查对象
        return obj


class ListView(generics.ListAPIView):
    queryset = Clothes.objects.select_related('color').all()  # 通过调试可以看出 避免n+1
    serializer_class = ClothesSerializer
    pagination_class = CustomPagination  # 分页器
    permission_classes = [permissions.AllowAny]
    # authentication_classes = [Authentication]
    versioning_class = APIVersioning  # api版本控制

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = ClothesFilter  # 自定义过滤

    parser_classes = [JSONParser, FormParser, ]  # 默认都解析

    # JSONParser：表示只能解析content-type:application/json的头
    # FormParser:表示只能解析content-type:application/x-www-form-urlencoded的头

    def get_queryset(self):
        data = self.request.query_params
        print(data)
        return super().get_queryset()
        # 可以通过版本号来控制queryset
        # version = self.request.version
        # if version == 'v1': ....

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response

# #############################################################################################################

# # 文件图片 视图
class UploadFileView(generics.CreateAPIView):
    serializer_class = MyFileSerializer
    # serializer_class = ListImgSerializer 解析多张文件视图的序列化器
    parser_classes = (
    MultiPartParser, FileUploadParser,)  # 解析file 使request.data包含file信息解析file_obj = request.data['file']
    # 注意如果前端传入多个files 一定要 file_objs = request.data.getlist('files') 否则只能获取一个


class UploadExcel(generics.CreateAPIView):
    """
    批量上传模型记录
    """
    serializer_class = ExcelSerializer
    parser_classes = (
        MultiPartParser, FileUploadParser,)  # 解析file 使request.data包含file信息解析file_obj = request.data['file']

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            ok = serializer.save()
            return JsResponse(ok)
        else:
            return JsResponse(data=serializer.errors, code=False)


class Download(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    header = {'邮箱': 'email', '用户': 'username'}

    def get_queryset(self):
        return self.queryset[:10]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        if not data:
            return JsResponse(msg = '你查询的数据不存在')
        else:
            return DataToExcel(headers=self.header, data=data).export


#### http缓存

from django.views.decorators.http import condition
import hashlib

"""
Last-Modified和Etags如何帮助提高性能?
　把Last-Modified 和ETags请求的http报头一起使用，这样可利用客户端（例如浏览器）的缓存。
  因为服务器首先产生 Last-Modified/Etag标记，服务器可在稍后使用它来判断页面是否已经被修改。
  本质上，客户端通过将该记号传回服务器要求服务器验证其（客户端）缓存。
过程如下:

客户端请求一个页面（A）。
服务器返回页面A，并在给A加上一个Last-Modified/ETag。
客户端展现该页面，并将页面连同Last-Modified/ETag一起缓存。
客户再次请求页面A，并将上次请求时服务器返回的Last-Modified/ETag一起传递给服务器。
服务器检查该Last-Modified或ETag，并判断出该页面自上次客户端请求之后还未被修改，直接返回响应304和一个空的响应体。
"""


# 这是通过 浏览器请求头中 etag值 来判断请求是否发生了变化 这里逻辑判断传入的参数是否变化 返回参数的hash值
def etag(request, *args, **kwargs):
    data = request.data or request.query_params
    return hashlib.md5(':'.join(dict(data).values()).encode('utf-8')).hexdigest()


# 这是通过 浏览器请求头中 Last-Modified 时间 来判断请求是否发生了变化 更新 这里返回更新时间
def last_modified(request, *args, **kwargs):
    data = request.data or request.query_params
    return Clothes.objects.last().updated_time


class HttpCacheView(APIView):  # 可以一起用 也可以只用一个 具体看实现逻辑
    @method_decorator(condition(etag_func=etag, last_modified_func=last_modified))
    def get(self, request, *args, **kwargs):
        data = request.data or request.query_params
        clothes = Clothes.objects.values()
        return JsResponse({'data': 'I have both Last-Modified and Etag!', 'clothes': clothes})


# 底层缓存
from django.core.cache import caches
from django.core.cache import cache  # 导入default 等价于 caches['default']


class CacheLow(APIView):

    def get(self, request, *args, **kwargs):
        cache = caches['account']
        cache.set('my_key', 'hello, world!', 30)
        cache.get('my_key')
        cache.get('my_key', 'has expired')
        # 使用 add() 方法可以添加键。它与 set() 带有相同的参数，但如果指定的键已经存在，将不会尝试更新缓存。
        cache.add('add_key', 'New value')

        cache.get_or_set('my_new_key', 'my new value', 100)

        cache.set_many({'a': 1, 'b': 2, 'c': 3})
        cache.get_many(['a', 'b', 'c'])

        cache.delete('a')
        cache.delete_many(['b', 'c'])

        """
        cache.clear()¶
        最后，如果你想删除缓存里的所有键，使用 cache.clear()。注意，clear() 将删除缓存里的 任何 键，不只是你应用里设置的那些键。

        >>> cache.clear()
        cache.touch(key, timeout=DEFAULT_TIMEOUT, version=None)¶
        New in Django 2.1.
        cache.touch() 为键设置一个新的过期时间。比如，更新一个键为从现在起10秒钟后过期：

        >>> cache.touch('a', 10)
        True
        和其他方法一样，timeout 参数是可选的，并且默认是 CACHES 设置的相应后端的 TIMEOUT 选项。

        如果键被成功 touch()，将返回 True，否则返回 False。

        cache.incr(key, delta=1, version=None)¶
        cache.decr(key, delta=1, version=None)¶
        你也可以使用分别使用 incr() 或 decr() 方法来递增或递减一个已经存在的键的值。默认情况下，存在的缓存值将递增或递减1。通过为递增/递减的调用提供参数来指定其他递增/递减值。如果你试图递增或递减一个不存在的缓存键，将会引发 ValueError 错误。

        >>> cache.set('num', 1)
        >>> cache.incr('num')
        2
        >>> cache.incr('num', 10)
        12
        >>> cache.decr('num')
        11
        >>> cache.decr('num', 5)
        6
        """

        return JsResponse(data='')


#######################################
# celery test
from .tasks import add
from celery_tasks.tasks import mul
import logging

logger = logging.getLogger('debug')


class CeleryAdd(APIView):

    def get(self, request, *args, **kwargs):
        try:
            result = add.apply_async(args=(2, 2), queue="default")
            # value = result.get()  # 等待任务执行完毕后，才会返回任务返回值 这是阻塞操作
            #
            # print(result.__dict__)  # 结果信息
            # print(result.successful())  # 是否成功
            # print(result.fail())  # 是否失败
            # print(result.ready())  # 是否执行完成
            # print(result.state)  # 状态 PENDING -> STARTED -> SUCCESS/FAIL
            # print(value)
            return JsResponse(data={'celery_id': result.id})
        except add.OperationalError as exc:  # 任务异常处理
            logger.exception('Sending task raised: %r', exc)
            return JsResponse(msg=f'Sending task raised: {exc}')


class CeleryMul(APIView):

    def get(self, request, *args, **kwargs):
        try:
            result = mul.apply_async(args=(2, 3), queue="task_heavy")
            return JsResponse(data={'celery_id': result.id})
        except mul.OperationalError as exc:  # 任务异常处理
            logger.exception('Sending task raised: %r', exc)
            return JsResponse(msg=f'Sending task raised: {exc}')
