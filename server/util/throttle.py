from rest_framework.throttling import SimpleRateThrottle

class VisitThrottle(SimpleRateThrottle):
    '''匿名用户60s只能访问三次（根据ip）'''
    scope = 'xxx'   #这里面的值，自己随便定义，settings里面根据这个值配置Rate

    def get_cache_key(self, request, view):
        #通过ip限制节流 获取ip
        return self.get_ident(request)

class UserThrottle(SimpleRateThrottle):
    '''登录用户60s可以访问10次'''
    scope = 'yyy'    #这里面的值，自己随便定义，settings里面根据这个值配置Rate

    def get_cache_key(self, request, view):
        return request.user.username


REST_FRAMEWORK = {
    # 自定义限制类   也可以直接继承  DRF 中 自带的限制
    # 'DEFAULT_THROTTLE_CLASSES' = ['auth_demo.throttle.MyThrottle'],

    # 使用内置限制类  的额外配置
    "DEFAULT_THROTTLE_RATES": {
        # key  与定义的 scope 对应 value: 5 表示次数 / m表示分钟  s秒  h小时  d天
        "xxx": "3/m",
        'yyy':'10/m'
    }
}


# 写在要配置的 视图中
throttle_classes = [VisitThrottle,]