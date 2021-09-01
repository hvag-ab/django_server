from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from util.excel import ExcelToModel
from .models import Colors, Clothes, MyFile
from django.contrib.auth.models import User

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
class ColorsSerializer(serializers.ModelSerializer):
    # clothes =  ClothesSerializer(many=True) #一对多需要用many
    favor = serializers.SerializerMethodField()  # 添加新的返回值

    class Meta:
        model = Colors
        fields = '__all__'

    def get_favor(self, obj):
        return obj.colors + '__hvag'


class ClothesSerializer(serializers.ModelSerializer):
    # 这里的外键包含OneToOneField ForeignKey  ManyToManyField
    color = ColorsSerializer()  # 首先关联的模型序列化 #多对一
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


# 自定义序列化 res=UserinfoSerializer(instance=users,many=True) #instance接受queryset对象或者单个model对象，当有多条数据时候，使用many=True,单个对象many=False
class UserinfoSerializer(serializers.Serializer):  # 定义序列化类
    id = serializers.IntegerField()  # 定义需要提取的序列化字段,名称和model中定义的字段相同
    username = serializers.CharField()
    rl = serializers.SerializerMethodField()  # 多对多序列化方法一

    def get_rl(self, obj):  # 名称固定：get_定义的字段名称
        """
        自定义序列化
        :param obj:传递的model对象，这里已经封装好的
        :return:
        """
        rl = 'hvag_' + obj.username # 获取所有的角色

        return {'rl':rl}  # 返回的结果一定是json可序列化的对象


# 二 参数验证 反序列化 dict - 模型
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=9,
        min_length=3,
        validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True)
    confirmpassword = serializers.CharField(required=True)
    random_no = serializers.CharField(write_only=True,required=False)

    # 单独验证某个字段
    def validate_password(self, password):
        # 注意参数，self以及字段名
        # 注意函数名写法，validate_ + 字段名字
        if len(password) >= 11:
            raise serializers.ValidationError("密码必须小于11岁")
        return password

    def validate(self, data):  ## data是传进来的参数 里面获取上面定义好的字段进行字段之间的验证，或者生成只读字段
        # 传进来什么参数，就返回什么参数，一般情况下用attrs
        if data['confirmpassword'] > data['password']:
            raise serializers.ValidationError("password must be equal")

        data['random_no'] = 'fsaifdsfiasdjfasifjsaf'  ##生成只读字段记录
        # del data['confirmpassword']
        return data

    def create(self, validated_data: dict):  # 添加数据
        # validated_data 里面包含就是你定义的验证字段属性 username password 。。。。
        # 注意，users在这里是放在上下文中的request，而不是直接的request 在序列化的时候 需要加入comtext = request 否则拿不到request
        # 例如 serializer = LoginSerializer(data=request.data, context={'request':request})
        request = self.context['request']  # 有时候需要request对象中的属性 例如 user=request.user
        passwrod = make_password(validated_data.get('password'))
        instance = User.objects.create(username=validated_data.get('username'),passwrod=passwrod)
        return instance

    def update(self, instance, validated_data):  # 更新数据
        # 更新的特别之处在于你已经获取到了这个对象instance 例如
        # serializer = LoginSerializer(data=request.data, instance=User.objects.get(username='hvag'), context={'request':request})
        instance.colors = validated_data.get('colors', instance.name)
        instance.save()
        return instance

    def save(self):  # 无论update or create 最终都是要调用save方法完成操作,可以重写save方法完成自己的逻辑
        request = self.context.get('request')
        validated_data = self.validated_data
        # do something


# 三  上传下载序列化 图片 文件 等
# 图片文件上传 验证
class MyFileSerializer(serializers.ModelSerializer):
    #
    image_url = serializers.ImageField(allow_empty_file=True,required=False)
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
        return {'view_imgs': images}  # 注意 这里的key一定是上面序列化的变量 因为这是序列化必须包含序列化定义的字段


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

        datas = ExcelToModel(file=file, header=self.header, serializer=LoginSerializer,
                             request=self.context['request']).excel2array
        # 如果数据量大 就批量导入
        for data in datas:
            print(type(data))  # dict
            # do something

        ok = True

        return {'ok': ok}  # 注意 这里的key一定是上面序列化的变量 因为这是序列化必须包含序列化定义的字段,
        # 不想被序列化的 一定要加上write_only=True   视图中 ok = serializer.save()
