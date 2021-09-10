from django.contrib import admin
from django.contrib.admin import ModelAdmin
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group,User
from . import models
from django.shortcuts import HttpResponse

admin.site.unregister(Token) # 不让Token模型显示
admin.site.unregister(Group)
admin.site.unregister(User) # 不让User模型显示 因为下面自定义User所以这里要取消默认的注册

"""
管理员admin 控制后台操作
可以新建多个账户 这些账户必须是激活账户 is_active=1  然后通过 User permissions: 授权给这些账户操作模型 否则没有权限操作模型
"""

@admin.register(models.Clothes)
class ClothModelAdmin(ModelAdmin):
    # 使用自定义的form表单验证功能
    # form = UserModelForm
    # 1.定义列表页面，显示列数据
    list_display = ['color', 'total', 'description','hvag']
    #自定义显示字段 自定义显示字段名 不能 和 模型中的字段名一样
    def hvag(self, obj):
        return obj.description

    hvag.empty_value_display = "默认为空时显示的值"

    # 2.定义列表页面，列可以进行点击进入编辑页面
    list_display_links = ['description']

    # 3.定义列表页面，快速搜索
    list_filter = ['created_time']

    # 4.定义列表页面，分页功能
    list_per_page = 10

    # 5. 列是否可编辑
    list_editable = ['color']

    # 6. 查询列
    search_fields = ['color', 'total']
    
    # 当存在多对多的外键的时候 设置这个 更加方便选择 可以填写多个外键字段
    filter_horizontal = ('外键字段',)

    # 7. 是否在页面顶端显示保存按钮
    # save_on_top = True

    # 8. 下拉选项的批量操作，类似于批量删除功能
    def func(self, request, queryset):
        print(self, request, queryset)
        id_list = request.POST.getlist('_selected_action')
        models.Clothes.objects.filter(id__in=id_list).delete()

    func.short_description = "批量初始化"

    actions = [func, 'export_as_excel']

    def export_as_csv(self, request, queryset):  # 具体的导出csv方法的实现
        return export_as_excel(self, request, queryset)

    export_as_csv.short_description = '导出Excel'  # 该动作在admin中的显示文字

    # Action选项都是在页面上方显示
    actions_on_top = True
    # Action选项都是在页面下方显示
    actions_on_bottom = False

    # 是否显示选择个数
    actions_selection_counter = True

    # raw_id_fields = ['ut',]
    # fields = ['name']
    # exclude = ['name',]

    # 10. 定义clothes模型内部编辑页面展示的字段
    # fieldsets = (
    #     ('基本数据', {
    #         'fields': ('description',)
    #     }),
    #     ('其他', {
    #         'classes': ('collapse', 'wide', 'extrapretty'),  # 'collapse','wide', 'extrapretty'
    #         'fields': ('color', 'total'),
    #     }),
    # )

    # fields = ('title', 'body','author','category')#显示可以编辑的字段 这个和fieldsets不能同时设定
    # exclude = ('author',)排除显示
    ordering = ['-id']

    # fk_fields 设置显示外键字段
    fk_fields = ('color',)

    date_hierarchy = 'created_time'  # 详细时间分层筛选　

    # raw_id_fields = ('FK字段', 'M2M字段',)

    """
    9. preserve_filters，详细页面，删除、修改，更新后跳转回列表后，是否保留原搜索条件

    10. save_as = False，详细页面，按钮为“Sava as new” 或 “Sava and add another”
    
    11. save_as_continue = True，点击保存并继续编辑
    
    6
    save_as_continue = True
     
    # 如果 save_as=True，save_as_continue = True， 点击Sava as new 按钮后继续编辑。
    # 如果 save_as=True，save_as_continue = False，点击Sava as new 按钮后返回列表。
        
        """

    readonly_fields = ('total',) #readonly_fields，详细页面时，只读字段

    autocomplete_fields = ['color']#取出外键数据 特别是对于有很多链接的外键
    
    def has_add_permission(self, request):
        # 禁用添加按钮
        return False

    def has_delete_permission(self, request, obj=None):
        # 禁用删除按钮
        return False

    def has_change_permission(self, request, obj=None):
        # 禁用编辑
        return False


class ClothesInline(admin.TabularInline):
    model = models.Ball
    extra = 1  # 默认内联显示条目的数量

@admin.register(models.Colors)
class ColorsModelAdmin(ModelAdmin):
    search_fields = ['colors']
    inlines = [ClothesInline]  # 内联 因为Clothes外键到Colors



## 当user是自己扩展的时候 为了在后台显示 跟原来的user一致
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.admin import UserAdmin #使用django自己的UserAdmin来注册
from django.utils.translation import gettext, gettext_lazy as _

class MyUserAdmin(UserAdmin):#解决自定义用户密码明文问题
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        # (_('phone'), {'fields': ('phone',)}),# 这里是你拓展的字段 编辑 第一个phone表示显示的标题栏 如果为none就表示不显示
    )
admin.site.register(User, MyUserAdmin)

from openpyxl import Workbook

def export_as_excel(self, request, queryset):
    meta = self.model._meta  # 用于定义文件名, 格式为: app名.模型类名
    field_names = [field.name for field in meta.fields]  # 模型所有字段名

    response = HttpResponse(content_type='application/msexcel')  # 定义响应内容类型
    response['Content-Disposition'] = f'attachment; filename={meta}.xlsx'  # 定义响应数据格式
    wb = Workbook()  # 新建Workbook
    ws = wb.active  # 使用当前活动的Sheet表
    ws.append(field_names)  # 将模型字段名作为标题写入第一行
    for obj in queryset:  # 遍历选择的对象列表
        for field in field_names:
            data = [f'{getattr(obj, field)}' for field in field_names]  # 将模型属性值的文本格式组成列表
        row = ws.append(data)  # 写入模型属性值
    wb.save(response)  # 将数据存入响应内容
    return response
