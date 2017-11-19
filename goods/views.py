from rest_framework import mixins
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from goods.models import GoodsProfile
from goods.serializer import GoodsProfileSerializer


class GoodsProfileViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    返回所有商品信息
    """
    queryset = GoodsProfile.objects.all()
    serializer_class = GoodsProfileSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'price', 'add_time')
