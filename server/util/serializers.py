from django.db import models
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
import re

"""
序列化器 serializers.Field 的通用参数 
参数名称	说明
read_only	表明该字段仅用于序列化输出，默认False  表示只返回，不写入数据库
write_only	表明该字段仅用于反序列化输入，默认False 表示只写入数据库 不返回给前端
required	表明该字段在反序列化时必须输入，默认True
default	序列化和反序列化时使用的默认值
allow_null	表明该字段是否允许传入None，默认False
validators	该字段使用的验证器
error_messages	包含错误编号与错误信息的字典
label	用于HTML展示API页面时，显示的字段名称
help_text	用于HTML展示API页面时，显示的字段帮助提示信息
max_length	最大长度
min_lenght	最小长度
allow_blank	是否允许为空
trim_whitespace	是否截断空白字符
max_value	最小值
min_value	最大值
source 指定某个外键的某个字段
"""



class Colors(models.Model):
    colors = models.CharField(max_length=10)

class Clothes(models.Model):
    color = models.ForeignKey("Colors", on_delete=models.CASCADE,related_name="clothes_color")  # 与颜色表为外键，颜色表为母表
    description = models.CharField(max_length=10, null=True)  # 描述


# 序列化
class ColorSerializer(serializers.Serializer):

    colors = serializers.CharField(
        max_length=11,
        min_length=11,
        validators=[UniqueValidator(queryset=Colors.objects.all())])
    lis = serializers.ListField(serializers.CharField(max_length=9), max_length=100, min_length=0)
    age = serializers.IntegerField(min_value=1, max_value=100,error_messages={'required':'age不能为空'})
    # format可以设置时间的格式，下面例子会输出如:2018-1-24 12:10
    pay_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    defualt_field = serializers.CharField(default="hvag",allow_blank=False)
    money = serializers.DecimalField(max_digits=6, decimal_places=4)
    #EmailField RegexField  URLField  FilePathField IPAddressField
    cho = serializers.ChoiceField(choices=((1,'h'),(2,'y')))
    js = serializers.JSONField()
    order_sn = serializers.CharField(write_only=True)
    ok = serializers.BooleanField(read_only=True)
    password = serializers.CharField(required=True)
    confirmpassword = serializers.CharField(required=True)

    def create(self, validated_data): # 添加数据
    # 除了用户，其他数据可以从validated_data这个字典中获取
    # 注意，users在这里是放在上下文中的request，而不是直接的request 在序列化的时候 需要加入comtext = request 否则拿不到request
    # 例如 serializer = SnippetSerializer(data=request.data, context={'request':request})
        user = self.context['request'].user
        age = validated_data['age ']
        instance = super().create(**validated_data)
        return instance

    def update(self, instance, validated_data): # 更新数据
    # 更新的特别之处在于你已经获取到了这个对象instance
        instance.colors = validated_data.get('colors',instance.name)
        instance.save()
        return instance

    def save(self):  # save并不一定是用来create或者 update 可以用来实现自己的逻辑
        request = self.context.get('request')
        token = request.query_params.get('token')
        # do something

    # 单独验证某个字段
    def validate_age(self, age):
        # 注意参数，self以及字段名
        # 注意函数名写法，validate_ + 字段名字
        if age <= 18:
            # REGEX_MOBILE表示手机的正则表达式
            raise serializers.ValidationError("age必须大于18岁")
        return age

    def validate(self, data): ## data是传进来的参数 里面获取上面定义好的字段进行字段之间的验证，或者生成只读字段
        # 传进来什么参数，就返回什么参数，一般情况下用attrs
        if data['confirmpassword'] > data['password']:
            raise serializers.ValidationError("password must be equal")

        data['order_sn'] = 'fsaifdsfiasdjfasifjsaf' ##生成只读字段记录
        return data


class ColorsSerializer(serializers.ModelSerializer):

    favor = serializers.SerializerMethodField() # 添加新的返回值

    class Meta:
        model = Colors
        fields = '__all__'

    def get_favor(self,obj):
        return obj.colors + '__hvag'

class ClothesSerializer(serializers.ModelSerializer):
    # 这里的外键包含OneToOneField ForeignKey  ManyToManyField
    color = ColorsSerializer() # 首先关联的模型序列化

    class Meta:
        model = Clothes
        fields = '__all__'

        # fields = []: 表示筛选字段
        # exclude = ('add_time',):  除去指定的某些字段
        # 这三种方式，存在一个即可
        # 表示连表的深度
        # depth = 1
        # read_only_fields = ('colors',)
        # extra_kwargs = {'password': {'write_only': True}}


#文件操作
class MyFile(models.Model):

    image_url = models.ImageField(upload_to='media/images/%Y/%m/%d', null=False, blank=False, verbose_name='图片url')
    file_url = models.FileField(upload_to='media/files/%Y/%m/%d', null=False, blank=False, verbose_name='文件url')

    class Meta:
        verbose_name = '文件'


class MyFileSerializer(serializers.ModelSerializer):
    #
    image_url = serializers.ImageField(allow_empty_file=True)
    file_url = serializers.FileField(allow_empty_file=True, use_url=True)

    class Meta:
        model = MyFile
        fields = ('image_url', 'file_url')

    def create(self, validated_data):
        file = validated_data.get('file_url')
        print(dir(file))
        print(file.size)
        print(file.name)
        return super().create(validated_data)


class ListImgSerializer(serializers.Serializer):
    imgs = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=True), write_only=True
    )
    view_imgs = serializers.ListField(
        child=serializers.CharField(max_length=1000, ), read_only=True
    )

    def create(self, validated_data):
        imgs = validated_data.get('imgs')
        images = []
        for index, image_url in enumerate(imgs):
            image = MyFile.objects.create(image_url=image_url)
            ima = MyFileSerializer(image, context=self.context)
            images.append(ima.data['image_url'])
        return {'view_imgs': images}  # 注意 这里的key一定是上面序列化的变量 因为这是序列化必须包含序列化定义的字段


# class SourceSerializer(serializers.Serializer):
#     """
#     批量上传序列化（excel）
#     """
#     excel = serializers.FileField(required=True, allow_empty_file=False, write_only=True,
#                                   error_messages={'empty': '未选择文件', 'required': '未选择文件'}, help_text="excel文件批量导入",
#                                   label="excel文件")
#
#     ok = serializers.CharField(read_only=True)
#
#     def create(self, validated_data):
#         file = validated_data.get('excel')
#         if not (
#                 file.content_type == 'application/vnd.ms-excel' or file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
#             raise serializers.ValidationError('请上传excel文件')
#
#         if file.size > 25 * 1024 * 1024:
#             raise serializers.ValidationError('上传文件过大')
#
#         serializer= SnippetSerializer
#         header = {'标题': 'title', '内容': 'code', 'linenos': 'linenos', '用户': 'username'}

#         model_serializer = SnippetUploadSerializer
#
#         datas = ExcelToModel(file=file, header=header, serializer=serializer,
#                               dict_data=True).excel_import_model
#
#         for data in datas:
#              print(type(data)) # dict
#              .... do something
#         Snippet.objects.bulk_create(models)
#
#         ok = True
#
#         return {'ok': ok}  # 注意 这里的key一定是上面序列化的变量 因为这是序列化必须包含序列化定义的字段,不想被序列化的 一定要加上write_only=True
#

