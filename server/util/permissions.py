from rest_framework import permissions


# example  视图 permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):## 控制整体权限 就是这个接口
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        #控制对象级别权限 也就是这个接口下某些数据记录 注意只有在has_permission通过后才能执行这条命令
        #这里的obj表示你查询的一条记录 模型的实例
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user





