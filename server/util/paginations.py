from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination
from rest_framework.response import Response


class MyPageNumberPagination(PageNumberPagination):
    #默认每页显示多少个
    page_size = 3
    #默认每页显示3个，可以通过传入pager1/?page=2&size=4,改变默认每页显示的个数 这是用户自定义页面数 用户自定义了 默认的就没用了
    page_size_query_param = "size"
    #每页最大显示数量，必须在 page_size_query_param 设置后才起效
    max_page_size = 10
    #获取页码数的
    page_query_param = "page"

    def get_paginated_response(self, data):#自定义分页器返回数据形式
        data =  {
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data,
            }

        return Response(status=200, data=dict(code=True, data=data))

