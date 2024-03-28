from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate

from util.file import ExcelToData
from .models import Colors, Clothes, MyFile

User = get_user_model()

"""
序列化器 serializers.Field 的通用参数 
参数名称	说明
read_only	表明该字段仅用于序列化输出，默认False  表示只返回，不写入数据库
write_only	表明该字段仅用于反序列化输入，默认False 表示只写入数据库 不返回给前端
required	表明该字段在反序列化时必须输入，默认True
default	序列化和反序列化时使用的默认值
format  时间序列化后的格式 例如 serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M') 输出如:2018-1-24 12:10
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
DecimalField(max_digits=6, decimal_places=4)
"""

# ModelSerializer这种尽量不用来做反序列化 模型里面常含有外键字段 外键字段需要排除exclude 否则容易报错
# 一.序列化 模型 - json  
# 1. 模型序列化


class ClothesSerializer(serializers.ModelSerializer):
    # 这里的外键包含OneToOneField ForeignKey  ManyToManyField
    # color = ColorsSerializer()  # 首先关联的模型序列化 #正向序列化 colors必须是Clothes属性
    # 另一种 只序列化一个外键模型的字段 color是Clothes 外键字段 然后拿关联的模型的colors字段值
    colors = serializers.CharField(source='color.colors')

    class Meta:
        model = Clothes
        fields = '__all__'

        # fields = []: 表示筛选字段
        # exclude = ('add_time',):  除去指定的某些字段
        # 这三种方式，存在一个即可
        # 表示连表的深度 1~10，建议使用不超过3
        # depth = 1


class ColorsSerializer(serializers.ModelSerializer):
    clothes_set = ClothesSerializer(many=True) #反向序列化 Clothes关联colors 写法 Clothes[.lower()]_set 也就是小写类名_set
    favor = serializers.SerializerMethodField()  # 添加新的返回值

    class Meta:
        model = Colors
        fields = '__all__'

    def get_favor(self, obj):
        return obj.colors + '__hvag'


# 二 参数验证 反序列化 dict - 模型
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=9,
        min_length=3,
        validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True)
    confirmpassword = serializers.CharField(required=True)

    # 单独验证某个字段
    def validate_password(self, password):
        # 注意参数，self以及字段名
        # 注意函数名写法，validate_ + 字段名字
        if len(password) >= 11:
            raise serializers.ValidationError("密码必须小于11位")
        return password

    def validate(self, data):  ## data是传进来的参数 里面获取上面定义好的字段进行字段之间的验证
        # 传进来什么参数，就返回什么参数，一般情况下用attrs
        if data['confirmpassword'] != data['password']:
            raise serializers.ValidationError("password must be equal")

        # del data['confirmpassword']
        return data

    def create(self, validated_data: dict):  # 添加数据
        # validated_data 里面包含就是你定义的验证字段属性 username password 。。。。
        # 注意，users在这里是放在上下文中的request，而不是直接的request 在序列化的时候 需要加入comtext = request 否则拿不到request
        # 例如 serializer = LoginSerializer(data=request.data, context={'request':request})
        request = self.context['request']  # 有时候需要request对象中的属性 例如 user=request.user
        # password = make_password(validated_data.get('password'))
        instance = User.objects.create_user(username=validated_data.get('username'),password=validated_data.get('password'))
        return instance


    def save(self):  # 无论update or create 最终都是要调用save方法完成操作,可以重写save方法完成自己的逻辑
        request = self.context.get('request')
        validated_data = self.validated_data
        # do something
        return super().save()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3)
    password = serializers.CharField(required=True)
    token = serializers.CharField(write_only=True,required=False) # 只读字段 传给前端 不写入表

    def validate(self, data):  ## data是传进来的参数 里面获取上面定义好的字段进行字段之间的验证，或者生成只读字段
        request = self.context['request']
        user = authenticate(request, username=data.get('username'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError("authenticate error")

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        token = api_settings.JWT_AUTH_HEADER_PREFIX + ' ' + token
        data['token'] = token  ##生成只读字段记录
        return data


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

    def update(self, instance, validated_data):  # 更新数据
        # 更新的特别之处在于你已经获取到了这个对象instance 例如
        # serializer = LoginSerializer(data=request.data, instance=User.objects.get(username='hvag'), context={'request':request})
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


# 三  上传下载序列化 图片 文件 等
# 图片文件上传 验证
class MyFileSerializer(serializers.Serializer):
    #
    image_url = serializers.ImageField(allow_empty_file=True,required=False)
    file_url = serializers.FileField(allow_empty_file=True, use_url=True)

    def create(self, validated_data):
        file = validated_data.get('file_url')
        image = validated_data.get('image')
        print(dir(file))
        print(file.size)
        print(file.name)
        File = MyFile.objects.create(file=file,image=image)
        return File


# 上传多张图片
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
        return {'view_imgs': images}  # 注意 这里的key一定是上面序列化的变量 因为这是序列化必须包含序列化定义的字段 返回值是serializer.save()


# 上传excel操作 序列化
# 例如批量注册 username  password confirmpassword
class ExcelSerializer(serializers.Serializer):
    """
    批量上传序列化（excel）
    """
    excel = serializers.FileField(required=True, allow_empty_file=False, write_only=True,
                                  error_messages={'empty': '未选择文件', 'required': '未选择文件'}, help_text="excel文件批量导入",
                                  label="excel文件")

    ok = serializers.CharField(read_only=True)
    header = {'用户名': 'username', '密码': 'password', '确认密码': 'confirmpassword'}

    def create(self, validated_data):
        file = validated_data.get('excel')
        if not (
                file.content_type == 'application/vnd.ms-excel' or file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
            raise serializers.ValidationError('请上传excel文件')

        if file.size > 25 * 1024 * 1024:
            raise serializers.ValidationError('上传文件过大')

        datas = ExcelToData(file=file, header=self.header).save

        for data in datas:
            print(type(data))  # dict
            # do something

        ok = True

        return {'ok': ok}  # 注意 这里的key一定是上面序列化的变量 因为这是序列化必须包含序列化定义的字段,
        # 不想被序列化的 一定要加上write_only=True   视图中 ok = serializer.save()
