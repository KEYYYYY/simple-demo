from datetime import datetime, timedelta

from rest_framework import serializers

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
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        """
        # 验证手机号是否存在
        if UserProfile.objects.filter(mobile=mobile):
            raise serializers.ValidationError('用户已经存在')

        # 验证手机号码是否合法
        if len(mobile) != 11:
            raise serializers.ValidationError('手机号码不合法')

        # 验证发送频率
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        if Code.objects.filter(add_time__gt=one_minute_ago, mobile=mobile):
            raise serializers.ValidationError('发送频率过快')

        return mobile
