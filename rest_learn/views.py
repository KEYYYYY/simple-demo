from random import randint

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .filters import GoodsFilter
from .models import Category, Code, Favorite, Goods, User
from .paginations import GoodsPagination
from .permissions import IsOwner
from .serializers import (CategorySerializer, CodeSerializer, GoodsSerializer,
                          UserDetailSerializer, UserFavSerializer,
                          UserRegSerializer)


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
    pagination_class = GoodsPagination
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
                  mixins.CreateModelMixin):
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
    """
    serializer_class = UserFavSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    # 在get_queryset之后作用
    lookup_field = 'goods_id'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
