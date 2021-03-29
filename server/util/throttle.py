from rest_framework.throttling import SimpleRateThrottle,BaseThrottle

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

# 5/min  5/hour 5/s 5/day
class AnonThrottle(AnonRateThrottle):
    THROTTLE_RATES = {"anon": "5/min"}


class UserThrottle(UserRateThrottle):
    THROTTLE_RATES = {"user": "30/min"}

# 视图中 throttle_classes = [AnonThrottle, UserThrottle]
# 这样的好处就是针对不同的视图限制访问频率

import random

# 随机限制
class RandomRateThrottle(BaseThrottle):
    def allow_request(self, request, view):
        return random.randint(1, 10) != 1


