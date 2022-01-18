from functools import wraps
from io import StringIO

from line_profiler import LineProfiler
from django.conf import settings


class profiler:

    def __init__(self, debug=True):
        self.debug = debug

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            lp = LineProfiler()
            lp_wrapper = lp(func)
            result = lp_wrapper(*args, **kwargs)
            fio = StringIO()
            lp.print_stats(stream=fio, stripzeros=True)
            if self.debug:
                print(fio.getvalue())
            else:
                file_path = settings.BASE_LOG_DIR / 'profile.log'
                with open(file_path, 'a') as f:
                    f.write(fio.getvalue())
            return result
        return wrapper
    
"""
使用：

class Test(APIView):

    @profiler
    def get(self, request, *args, **kwargs):
        func1(..)
        func2(..)
        
如果发现func1 函数处理慢
@profiler
func1  查看具体

"""
