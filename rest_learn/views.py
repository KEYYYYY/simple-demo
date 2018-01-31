from random import randint

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .filters import GoodsFilter
from .models import (Category, Code, Favorite, Goods, Order, ShoppingItem,
                     User, UserAddress)
from .paginations import GenericPagination
from .permissions import IsOwner
from .serializers import (AddressSerializer, CategorySerializer,
                          CodeSerializer, GoodsSerializer, OrderSerializer,
                          ShoppingItemDetailSerializer, ShoppingItemSerializer,
                          UserDetailSerializer, UserFavDetailSerializer,
                          UserFavSerializer, UserRegSerializer, OrderDetailSerializer)


class GoodsViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):
    """
    list:
        获取所有商品信息
    retrieve:
        获取某个商品详细信息
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GenericPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'category__name')
    ordering_fields = ('add_time', 'update_time', 'price')


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin):
    """
    list:
        得到所有商品类别
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CodeViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin):
    """
    create:
        发送验证码接口
    """
    serializer_class = CodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 生成验证码
        code = ''.join(str(randint(0, 9)) for _ in range(6))
        # 记录验证码和手机号
        Code.objects.create(
            code=code, mobile=serializer.validated_data['mobile'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin):
    """
    create:
        用户注册
    retrieve:
        获得某一用户详细信息
    """
    queryset = User.objects.all()

    # 每个不同的方法有不同的权限
    # post允许任何人
    # get只允许登陆用户获得自己的信息
    # 动态判断permission
    def get_permissions(self):
        # 只有viewset才会有action
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.AllowAny()]

    # 每个方法用到的序列化类也不同
    # 动态设置serializer
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegSerializer
        if self.action == 'retrive':
            return UserDetailSerializer
        return UserDetailSerializer


class UserFavViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    """
    list:
        得到当前用户的收藏列表
    create:
        为当前用户创建一个收藏项
    destory:
        删除当前用户的一个收藏项
    retrieve:
        得到当前用户是否收藏该商品
    """
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    # 在get_queryset之后作用
    lookup_field = 'goods_id'
    pagination_class = GenericPagination

    # 创建、删除收藏只需要提供商品ID和用户ID
    # 得到收藏列表需要得到商品的详细情况
    # 所以动态设置序列化类
    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        else:
            return UserFavSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class AddressViewSet(viewsets.ModelViewSet):
    """
    list:
        得到该用户的所有收货地址
    create:
        增加收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    retrieve:
        得到某个收货地址详情
    """
    permissions_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    list:
        得到该用户的所有购物车货物
    create:
        增加一个商品
    update:
        更新商品数量
    delete:
        删除购物车商品
    retrieve:
        得到商品详情
    """
    permissions_classes = (permissions.IsAuthenticated, IsOwner)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingItemDetailSerializer
        else:
            return ShoppingItemSerializer

    def get_queryset(self):
        return ShoppingItem.objects.filter(user=self.request.user)


class OrderViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):
    """
    list:
        得到该用户的所有订单
    create:
        创建一个订单
    delete:
        删除一个订单
    retrieve:
        获取一个订单的详细
    """
    permissions_classes = (permissions.IsAuthenticated, IsOwner)

    # retrieve的时候需要详细的商品列表
    # 所以动态设置序列化类
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        else:
            return OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
