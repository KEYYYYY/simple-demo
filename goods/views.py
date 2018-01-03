from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from goods.models import GoodsProfile, Category
from goods.serializer import GoodsProfileSerializer, CategorySerializer
from goods.filters import GoodsProfileFilter


class GoodsProfileViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    返回所有商品信息
    """
    queryset = GoodsProfile.objects.all()
    serializer_class = GoodsProfileSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = GoodsProfileFilter
    ordering_fields = ('price', 'add_time')


class CategoryViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """
    返回所有类别信息
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
