from datetime import datetime, timedelta

from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Goods, Category, UserProfile, Code


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Goods
        fields = '__all__'


class CodeSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True, min_length=11, max_length=11)

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
    code = serializers.CharField(
        write_only=True, required=True, min_length=6, max_length=6)
    mobile = serializers.CharField(min_length=11, max_length=11)
    password = serializers.CharField(
        write_only=True, min_length=3, max_length=32)

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

    class Meta:
        model = User
        fields = ('username', 'password', 'mobile', 'code')
