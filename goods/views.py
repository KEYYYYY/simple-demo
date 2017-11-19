from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from goods.models import GoodsProfile
from goods.serializer import GoodsProfileSerializer


class GoodsProfileView(APIView):
    """
    返回所有商品信息
    """

    def get(self, request, format=None):
        goods_profiles = GoodsProfile.objects.all()
        serlalizer = GoodsProfileSerializer(
            goods_profiles,
            # 返回数组
            many=True
        )
        return Response(serlalizer.data)

    def post(self, request, format=None):
        serializer = GoodsProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
