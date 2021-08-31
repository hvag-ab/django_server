from rest_framework import permissions


# example  视图 permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
"""
执行顺序是现验证token session 然后在执行权限认证
可以获取request的属性
例如
# user = self.request.user
# data = self.request.data or self.request.query_params # 获取get or post delete请求方法传递过来的参数
还可以给request绑定属性
例如
返回True的前面添加 request.hvag = "hvag"  这样后面的视图获取request方法的时候 直接拿这个属性 达到传递变量的作用
view参数 是获取视图的类属性方法
class x(APIView):
   params = "x"
 p = getattr(view,'params') == 'x'
"""
class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):## 控制整体权限 就是这个接口
        request.hvag = "hvag"
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        #控制对象级别权限 也就是这个接口下某些数据记录 注意只有在has_permission通过后才能执行这条命令
        #这里的obj表示你查询的一条记录 模型的实例
        # 视图调用def get_object(self):
        #     obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        #     self.check_object_permissions(self.request, obj)
        #     return obj
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user





