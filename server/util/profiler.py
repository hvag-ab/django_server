from functools import wraps

try:
    from line_profiler import LineProfiler
    from io import StringIO
except ImportError:
    pass


def profiler(use=True):
    def deco_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if use:
                lp = LineProfiler()
                lp_wrapper = lp(func)
                result = lp_wrapper(*args, **kwargs)
                fio = StringIO()
                lp.print_stats(stream=fio, stripzeros=True)
                print(fio.getvalue())
            else:
                result = func(*args, **kwargs)
            return result

        return wrapper

    return deco_func
    
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
