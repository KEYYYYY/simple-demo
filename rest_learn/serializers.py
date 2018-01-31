from datetime import datetime, timedelta
from time import strftime

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (Category, Code, Favorite, Goods, GoodsImage, UserAddress,
                     UserProfile, ShoppingItem, Order, OrderGoods)
from utils import defaults


class CategorySerializer(serializers.ModelSerializer):
    """
    商品类别序列化类
    """
    add_time = serializers.DateTimeField(
        read_only=True, format='%Y-%m-%d %H:%M'
    )
    update_time = serializers.DateTimeField(
        read_only=True, format='%Y-%m-%d %H:%M'
    )

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
    add_time = serializers.DateTimeField(
        read_only=True, format='%Y-%m-%d %H:%M'
    )
    update_time = serializers.DateTimeField(
        read_only=True, format='%Y-%m-%d %H:%M'
    )

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
    """
    用户信息序列化类
    """
    class Meta:
        model = UserProfile
        fields = ('mobile',)


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    id = serializers.HiddenField(
        default=defaults.CurrentUserIDDefault(),
    )
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'userprofile')

    # 当字段内包含其他序列化类的时候需要自定义update
    def update(self, instance, validated_data):
        profile = instance.userprofile
        instance.username = validated_data['username']
        profile.mobile = validated_data['userprofile']['mobile']
        instance.save()
        profile.save()
        return instance


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


class UserFavDetailSerializer(serializers.ModelSerializer):
    """
    用户收藏详情序列化类
    """
    goods = GoodsSerializer()

    class Meta:
        model = Favorite
        fields = ('id', 'goods')


class AddressSerializer(serializers.ModelSerializer):
    """
    用户收货地址序列化类
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M', read_only=True
    )

    class Meta:
        model = UserAddress
        fields = '__all__'


class ShoppingItemSerializer(serializers.ModelSerializer):
    """
    购物车商品项目序列化类
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(
        min_value=1
    )
    is_from_cart = serializers.BooleanField(
        write_only=True, default=False,
        help_text='是否从购物车中操作',
    )

    # 不删除额外字段创建会出错
    def create(self, validated_data):
        del validated_data['is_from_cart']
        return super(ShoppingItemSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        instance.user = self.context['request'].user
        instance.goods_id = validated_data['goods']
        if validated_data['is_from_cart']:
            instance.nums = validated_data['nums']
        else:
            instance.nums += validated_data['nums']
        instance.save()
        return instance

    class Meta:
        model = ShoppingItem
        fields = '__all__'


class ShoppingItemDetailSerializer(serializers.ModelSerializer):
    """
    购物车项目详情序列化类
    """
    goods = GoodsSerializer()

    class Meta:
        model = ShoppingItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """
    订单序列化类
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(
        read_only=True,
        format='%Y-%m-%d %H:%M',
    )

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('status', 'sn', 'order_mount')

    def create(self, validated_data):
        from random import randint
        shopping_items = ShoppingItem.objects.filter(
            user=self.context['request'].user
        )
        # 生成订单号
        sn = '{time}{user_id}{random_str}'.format(
            time=strftime('%Y%m%d%H%M%S'),
            user_id=self.context['request'].user.id,
            random_str=str(randint(1000, 4000))
        )
        validated_data['sn'] = sn
        order = Order.objects.create(**validated_data)
        order_mount = 0
        # 遍历购物车每一个项目，设置订单物品项目
        for shopping_item in shopping_items:
            order_goods = OrderGoods()
            order_goods.goods = shopping_item.goods
            order_goods.order = order
            order_goods.nums = shopping_item.nums
            # 计算订单金额
            order_mount += shopping_item.nums * shopping_item.goods.price
            order_goods.save()
            # 从购物车清除
            shopping_item.delete()
        order.order_mount = order_mount
        order.save(update_fields=('order_mount',))
        return order


class OrderGoodsSerializer(serializers.ModelSerializer):
    """
    订单商品序列化类
    """
    goods = GoodsSerializer()

    class Meta:
        model = OrderGoods
        fields = ('goods', 'nums')


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    订单详情序列化类
    """
    order_goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
