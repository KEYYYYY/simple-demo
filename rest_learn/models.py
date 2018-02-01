from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=11, verbose_name='手机号')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name='名称')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='goods',
        verbose_name='类别'
    )
    name = models.CharField(max_length=128, verbose_name='商品名称')
    price = models.FloatField(verbose_name='商品价格')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)

    def __str__(self):
        return self.name


class Code(models.Model):
    code = models.CharField(max_length=6, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class GoodsImage(models.Model):
    goods = models.ForeignKey(
        Goods, on_delete=models.CASCADE,
        related_name='images', verbose_name='商品名称'
    )
    image = models.ImageField(
        upload_to='media/goods_images/', verbose_name='轮播图')
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '商品轮播图'
        verbose_name_plural = verbose_name

    def __str(self):
        return self.goods.name


class Favorite(models.Model):
    goods = models.ForeignKey(
        Goods, on_delete=models.CASCADE, verbose_name='商品'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='用户'
    )
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        unique_together = ('goods', 'user')


class UserAddress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='用户'
    )
    district = models.CharField(
        max_length=128, blank=False, verbose_name='区域'
    )
    address = models.CharField(
        max_length=256, blank=False, verbose_name='详细地址'
    )
    mobile = models.CharField(
        max_length=11, blank=False, verbose_name='收货人联系方式'
    )
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)

    def __str__(self):
        return self.user.username


class ShoppingItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='用户'
    )
    goods = models.ForeignKey(
        Goods, on_delete=models.CASCADE, verbose_name='商品'
    )
    nums = models.IntegerField(default=1, verbose_name='数量')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '购物车项'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)
        unique_together = ('user', 'goods')

    def __str__(self):
        return self.goods.name


class Order(models.Model):
    STATUS = (('w', '待支付'), ('r', '已支付'))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='用户',
    )
    sn = models.CharField(
        null=True, max_length=32, verbose_name='订单号',
    )
    # 这里不推荐使用外键指向一个地址
    # 因为用户可能在提交订单后修改了自己的地址
    # 会造成订单数据变动
    address = models.CharField(
        max_length=256, verbose_name='配送地址',
    )
    status = models.CharField(
        max_length=1, choices=STATUS, default='w',
        verbose_name='支付状态',
    )
    order_mount = models.FloatField(
        default=0, verbose_name='订单金额'
    )
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)


class OrderGoods(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name='订单',
        related_name='order_goods',
    )
    goods = models.ForeignKey(
        Goods, on_delete=models.SET_NULL, null=True,
        verbose_name='商品',
    )
    nums = models.IntegerField(
        verbose_name='商品数量',
    )

    class Meta:
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    """
    轮播图模型
    """
    goods = models.ForeignKey(
        Goods, on_delete=models.CASCADE, verbose_name='商品',
    )
    image = models.ImageField(
        upload_to='media/banners', verbose_name='图片',
    )
    index = models.IntegerField(
        default=0, verbose_name='顺序',
    )
    add_time = models.DateTimeField(
        auto_now_add=True, verbose_name='添加时间',
    )

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
