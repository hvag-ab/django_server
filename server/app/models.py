from django.db import models
# from django.db.models import CheckConstraint, UniqueConstraint
from django.db.models.signals import post_save
from django.dispatch import receiver


class BaseModel(models.Model):
    updated_time = models.DateTimeField(auto_now=True) # 无论更新or添加都会更改时间
    created_time = models.DateTimeField(auto_now_add=True) # 添加才会更改时间

    class Meta:
        # 基表，为抽象表，是专门用来被继承，提供公有字段的，自身不会完成数据库迁移
        abstract = True


class Colors(BaseModel):
    colors = models.CharField(max_length=10)  # 蓝色

    def __str__(self):
        return self.colors

    class Meta:
        db_table = "colors"  # 在数据库中的表名 当使用数据库已经存在表的时候 可以用这个字段指定哪个表
        # ordering = ('id',) #按照某些字段排序
        # permissions = (('定义好的权限', '权限说明'),)
        # 给数据库的表设置额外的权限
        # managed = True  # 如果为false django只能查询这个表 不能增删改
        # unique_together = ('id', 'colors') #联合唯一键
        # constraints = [
        #     CheckConstraint(
        #         check=~models.Q(colors ="red") & models.Q(colors__contains="_color"),
        #         name="not red and contains color"),## 条件约束
        # UniqueConstraint(fields=['id', 'colors'], name='unique_color'),### 联合唯一约束
        # UniqueConstraint(fields=['colors'], condition=models.Q(colors='red'), name='red') ## 条件约束
        # ]

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):  # 模型保存or更新时 执行其他逻辑 仅试用单条记录创建or更新
        
        # if self.pk: 添加   if not self.pk 表示更新
        #     do something
        
        #在批量创建或更新时 不会调用save（）、pre_save和post_save
        
        """单条记录更新
        _t = Colors.objects.get(id=pk)
        _t.__dict__.update(**colors)
        _t.save()
        
        # 单条记录创建  Colors.objects.create(**colors)
        """

        super().save(force_insert, force_update, using,
                     update_fields)

    def delete(self, using=None, keep_parents=False): # 单条记录删除的情况下调用 Colors.objects.get(id=pk).delete()
        # do something
        # 当批量删除的时候，不会调用model的delete()方法，但delete是可以使用pre_delete或post_delete信号的
        return super().delete(using, keep_parents)  # 模型执行删除时 执行其他逻辑


class Ball(models.Model):
    color = models.OneToOneField("Colors", on_delete=models.CASCADE, related_name="ball_color")  # 与颜色表为一对一，颜色表为母表
    description = models.CharField(max_length=10)  # 描述

    def __str__(self):
        return self.description


class Clothes(BaseModel):
    color = models.ForeignKey("Colors", on_delete=models.CASCADE, related_name="clothes_color")  # 与颜色表为外键，颜色表为母表
    description = models.CharField(max_length=10, null=True)  # 描述
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.description


class Child(models.Model):
    name = models.CharField(max_length=10)  # 姓名
    favor = models.ManyToManyField('Colors', related_name='child_favor')  # 与颜色表为多对多
    
    
"""
from pathlib import Path
from secrets import token_hex
from django.utils.deconstruct import deconstructible
# 主要是防止不同用户传文件  文件重名导致覆盖
@deconstructible
class TimeStampFileName:
    def __init__(self, path):
        self.path = Path(path)

    def __call__(self, instance, filename):
        filename = Path(filename)
        extension = filename.suffix
        file_stem = f"{filename.stem}_{token_hex(8)}"
        return str(self.path / file_stem) + extension
"""

#文件操作
class MyFile(models.Model):

    image_url = models.ImageField(upload_to='media/images/%Y/%m/%d', null=False, blank=False, verbose_name='图片url')
    file_url = models.FileField(upload_to=TimeStampFileName('media/'), null=False, blank=False, verbose_name='文件url')
    #实际的路径就是 MEDIA_ROOT/{upload_to}/filename
    #所以可以用uoload_to来指定文件存放的前缀路径

# 枚举
class EnumModel(models.Model):
    class Paid(models.IntegerChoices):
        wx = 0, '微信'
        ali = 1, '支付宝'
        other = 2, '其他'

    pay_by = models.PositiveSmallIntegerField('支付方式', choices=Paid.choices, default=Paid.wx)
"""
Paid.choices --------- [(0, '微信'), (1, '支付宝'), (2, '其他')]
Paid.labels  -------------- ['微信', '支付宝', '其他']   Paid.names - ['wx','ali','other]  Paid.values -- [0,1,2]
Paid.wx.label --  '微信'  Paid.wx.value --- 0  Paid.wx.name -- wx
obj = EnumModel.objects.create(pay_by=0)
assert obj.pay_by == obj.Paid.wx == 0
# 枚举参数检验 如果不检验直接存 那么也会存进去就会造成脏数据   应该判断 例如 if 3 in EnumModel.Paid: EnumModel.objects.create(pay_by=3)
或者存入枚举类  EnumModel.objects.create(EnumModel.Paid.ali)
"""



# 信号
@receiver(post_save, sender=Colors)
def create_user_token(sender, instance=None, created=False, **kwargs):
    if created:  # 如果Colors创建一条记录那么
        Clothes.objects.create(color=instance)  #


"""
Django项目中经常使用到信号，但使用信号的代码更难阅读和维护。在保持不同模型数据同步更新时，
到底使用信号signals，还是重写save方法更好？建议：

当你的字段依赖于一个你可以控制的模型，推荐使用重写 .save
如果你的字段依赖于一个你不能控制第三方app的模型，使用信号。

ForeignKey 参数说明
to_field 表示指定关联另一个表的哪一个字段 被关联的字段必须是唯一建 默认是关联到主键上
db_constraint  表示是否在数据库层面建立外键 false表示不在数据库层面建立 这种可以在已有的两表中建立外键关系，If this is set to False, accessing a related object that doesn't exist will raise its DoesNotExist exception.
related_name 关联名 表示反向查询时用的名称
db_column='hvag' 指定这个字段在表中对应哪个字段名称,如果不指定 外键默认变成hvag_id 
特别说明
一旦作为外键的字段例如hvag 那么在数据库中就会默认变成 hvag_id _id是django添加的 用来保存被关联的表的字段对应的值 
这点很容易在已有表中出现错误，
因为这个问题 导致在已有表中不能建立django的外键关系 db_column需要这个参数来指定为需要作为外键的名字

on_delete在外建中必须设置，表示级联关系，

CASCADE：默认值，级联
 例子：作者被删，作者详情一定没有
DO_NOTHING：外键不会被级联，假设A表依赖B表，B记录删除，A表的外键字段不做任何处理
例子：作者被删了，作者的书还存在，书还是该作者写的；出版社没了，出版社出版的书还在
SET_DEFAULT：假设A表依赖B表，B记录删除，A表的外键字段重置为default属性设置的值，所以必须配合default属性使用。
例子：部门没有了，部门员工里的部门字段改为未分组部门的id
SET_NULL使用的时候需要blank=True, null=True；假设A表依赖B表，B记录删除，A表的外键字段重置为NULL，所以必须配合NULL=True使用。
 例子：部门没有了，部门员工里的部门字段改为未分组部门的id字段为NULL
注：多对多字段不能设置on_delete级联关系，如果要处理级联关系，需要手动明确关系，处理表关系中的多个外键
如果使用两个表之间存在关联,首先db_constraint=False 把关联切断,但保留链表查询的功能,其次要设置null=True, blank=True,注意on_delete=models.SET_NULL 一定要置空,这样删了不会影响其他关联的表

"""

"""
一对多查询
# 正向
1.cloth = Clothes.objects.select_related('color').get(description="hvag")
print(cloth.color.colors)
2.cloth = Clothes.objects.select_related('color').filter(color__colors="red")
print(cloth[0].description)
3.Clothes.objects.filter(color__colors="red").values('color__colors','description'))
4.color_obj=models.Colors.objects.get(colors="红") print(color_obj.clothes_set.all())  如果设置了related_name='hvag' print(color_obj.hvag.all())

# 反向
cloths = Clothes.objects.filter(color=Colors.objects.get(colors="红")))

add
Clothes.objects.create(color=models.Colors.objects.get(colors="green"),description="xxxy")

跟查询用法一样 先查询后才能update or delete
update
Clothes.objects.filter(color__colors="red").update(description="大美女")

delete
Clothes.objects.get(description="灰裙子").delete()

一对一查询
# 正向
1.Ball.objects.select_related('color').get(description="红球").color.colors
# 反向
2.Colors.objects.get(ball__description="红球").colors
3.Colors.objects.get(colors="红").ball.description # 注意反向的时候 ball 是 字表的类名的小写 写法："母表对象.子表表名的小写.子表字段名"；

增删改 跟上面一对多类似

多对多查询
# 正向
ch = Child.objects.prefetch_related('favor').get(name='a')
for i in ch.favor.all():
    print(i.colors)

Child.objects.filter(favor=Colors.objects.get(colors="黄"))

# 反向
color_obj = Colors.objects.get(colors="黄")
print(color_obj.child_favor.all())

母表对象.filter(子表表名小写__子表字段名="过滤条件")
Colors.objects.filter(child__name="a")

增 和 改 
正向
Child.objects.create(name="b").favor.add(*(Colors.objects.all()))
改
ch = Child.objects.get(name="b")
ch.favor = Colors.objects.get(...) ch.save()

反向
ch = Child.objects.create(name="c")
color = Colors.objects.get(c_name="c")
color.child_favor.add(ch)

chs = Child.objects.all()
color = Colors.objects.get(c_name="c")
color.child_favor.add(*chs)

删
#删除子表数据
color = Colors.objects.get(c_name="c")
color.child_favor.all().delete()
Child.objects.delete()

删除母表与子表关联关系
color = Colors.objects.get(c_name="c")
color.child_favor.clear()
"""

# 自定义user
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth import get_user_model
#
#
# # Create your models here.
# class Profile(AbstractUser):
#     phone = models.CharField(max_length=11)


# settings.py

# AUTH_USER_MODEL = 'youpath.Profile'

# 后续需要用到user模型 需要 使用 User = get_user_model()

"""
## 获取模型元数据


meta = Book._meta

db_table = meta.db_table

model_name = str(meta)
fields_name = meta.field.name
field_names = [field.name for field in meta.fields]  # 模型所有字段名
print(dir(meta))
"""
