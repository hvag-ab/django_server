import django_filters
from .models import Clothes,Colors

# django_filters 入口是 视图中 self.filter_queryset 方法

class ClothesFilter(django_filters.FilterSet):

    total = django_filters.NumberFilter(field_name='total',lookup_expr='exact') # 精确查找
    description = django_filters.CharFilter(field_name='description',lookup_expr='icontains') # 忽略大小写模糊查找 contains 不忽略大小写模糊查找
    total_gt = django_filters.NumberFilter(field_name='total', lookup_expr='gt') # gt 大于  gte 大于等于 lt小于 lte小于等于
    total_lte = django_filters.NumberFilter(field_name='total', lookup_expr='lte', required=True) #required参数必须

    created_year = django_filters.NumberFilter(field_name='created_time', lookup_expr='year') #类似orm中取年部分
    created_year__gt = django_filters.NumberFilter(field_name='created_time', lookup_expr='year__gt') #取年部分且大于

    id_range = django_filters.NumericRangeFilter(field_name='id', lookup_expr='range') # id_range_min=1&id_range_max=3
    total_range = django_filters.NumericRangeFilter(field_name="total",lookup_expr='range', exclude=True)  # 反逻辑 不在这个区间中 如果是false就是在这个区间中

    date = django_filters.DateTimeFromToRangeFilter(field_name='updated_time',lookup_expr='range')
    # 查询条件  date_after=2016-01-01&date_before=2016-02-01  或者 date_after=2016-01-01 或者 date_before=2016-02-01
    # 含有外键
    colors = django_filters.CharFilter(field_name='color__colors', lookup_expr='icontains')
    # 排序 GET /user/users/?sort=-id: -表示降序，+升序  如果多个排序字段 sort=[id,-total]
    sort = django_filters.OrderingFilter(fields=('id',))


    # has_category = django_filters.BooleanFilter(field_name='category', lookup_expr='isnull', exclude=True) #反逻辑


    class Meta:
        model = Clothes
        # 一定要写你用了哪些字段来筛选 否则报错
        fields = ['total','id','color__colors','description']
        """
        也可以简写
        # fields = {
            # "description": ['exact','icontains'],
            # "id": ['exact'],
        # }
        """

class ColorsFilter(django_filters.FilterSet):

    # 自定义查询 目的是把传入的值转化成model需要的查询值
    total = django_filters.NumberFilter(field_name='total',method='get_total')

    class Meta:
        model = Colors
        # 一定要写你用了哪些字段来筛选 否则报错 这里的字段一定是model里面的字段
        # 如果使用了自定义查询 那么就是自定义查询中queryset过滤里面的model字段 如果没有自定义查询 那么就是filed_name指定的字段
        fields = ['colors']

    def get_total(self, queryset, name, value):
        # name 参数 是上面定义的 field_name的值 value是你传入的值 例如 total = 1   name="total"  value =1
        # queryset参数是 你视图中 queryset设置的orm查询对象
        # 可以获取request 及其 request的属性
        # user = self.request.user
        # data = self.request.data or self.request.query_params
        if value is None:
            return queryset
        cs = Clothes.objects.filter(total=value).values_list('color__colors')
        if cs:
            return queryset.filter(**{'colors__in':cs})
        return queryset

    # 全局过滤queryset 例如排除 红色 # 在前面条件过滤之后执行这个方法
    @property
    def qs(self):
        queryset = super().qs
        user = getattr(self.request, 'user', None)

        return queryset.exclude(colors ='red')

"""
  # 非restful 情况下
f = ColorsFilter(request.GET, queryset=Colors.objects.all())
"""
