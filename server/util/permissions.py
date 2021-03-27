from rest_framework import permissions


# 只读，作者可修改
class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):## 控制整体权限 就是这个接口
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.session.get('user_id') is not None

    def has_object_permission(self, request, view, obj): #控制对象级别权限 也就是这个接口下某些数据记录 注意只有在has_permission通过后
        #才能执行这条命令
        # 通过源码可以知道 SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS') 这三个模式就是只读模式
        if request.method in permissions.SAFE_METHODS:
            return True
        # 如果不满足safe methods  那么再看满不满足第二个条件
        return obj.author == request.user





