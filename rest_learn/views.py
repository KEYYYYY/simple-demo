from random import randint

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter

from .filters import GoodsFilter
from .models import Category, Goods, Code
from .serializers import CategorySerializer, CodeSerializer, GoodsSerializer


class GoodsViewSet(viewsets.ModelViewSet):
    """
    返回所有商品信息
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'category__name')
    ordering_fields = ('add_time', 'update_time', 'price')


class CategoryViewSet(viewsets.ModelViewSet):
    """
    返回所有类别的信息
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CodeViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin):
    """
    接受电话号码接口
    """
    serializer_class = CodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 生成验证码
        code = ''.join(str(randint(0, 9)) for _ in range(6))
        print(code)
        # 记录验证码和手机号
        Code.objects.create(
            code=code, mobile=serializer.validated_data['mobile'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
