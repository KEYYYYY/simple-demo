from datetime import datetime, timedelta

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category, Code, Favorite, Goods, GoodsImage, UserProfile


class CategorySerializer(serializers.ModelSerializer):
    """
    商品类别序列化类
    """
    class Meta:
        model = Category
        fields = '__all__'


class GoodsImageSerializer(serializers.ModelSerializer):
    """
    商品图片序列化类
    """
    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    """
    商品序列化类
    """
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = '__all__'


class CodeSerializer(serializers.Serializer):
    """
    验证码序列化类
    """
    mobile = serializers.CharField(
        required=True, min_length=11, max_length=11,
        help_text='电话号码'
    )

    def validate_mobile(self, mobile):
        """
        验证手机号码
        """
        # 验证手机号是否存在
        if UserProfile.objects.filter(mobile=mobile):
            raise serializers.ValidationError('用户已经存在')

        # 验证手机号码是否合法
        # xxxx

        # 验证发送频率
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        if Code.objects.filter(add_time__gt=one_minute_ago, mobile=mobile):
            raise serializers.ValidationError('发送频率过快')

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册序列化类
    """
    username = serializers.CharField(
        read_only=True,
    )
    code = serializers.CharField(
        write_only=True, required=True, min_length=6, max_length=6,
        help_text='验证码'
    )
    mobile = serializers.CharField(
        write_only=True, min_length=11, max_length=11,
        help_text='电话号码'
    )
    password = serializers.CharField(
        write_only=True, min_length=3, max_length=32
    )

    def validate_code(self, code):
        last_code = Code.objects.filter(
            code=code,
            mobile=self.initial_data['mobile']
        ).order_by('-add_time').first()
        if last_code:
            if last_code != code:
                serializers.ValidationError('验证码不正确')
        else:
            raise serializers.ValidationError('验证码不正确')
        return code

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        mobile = validated_data['mobile']
        user = User.objects.create_user(
            username=username,
            password=password
        )
        UserProfile.objects.create(user=user, mobile=mobile)
        return user

    def validate(self, attrs):
        attrs['username'] = attrs['mobile']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'mobile', 'password', 'code')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('mobile',)


class UserDetailSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'userprofile')


class UserFavSerializer(serializers.ModelSerializer):
    """
    用户收藏序列化类
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Favorite
        fields = '__all__'
