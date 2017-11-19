from rest_framework import generics

from goods.models import GoodsProfile
from goods.serializer import GoodsProfileSerializer


class GoodsProfileView(generics.ListAPIView):
    """
    返回所有商品信息
    """
    queryset = GoodsProfile.objects.all()
    serializer_class = GoodsProfileSerializer
