from rest_framework import serializers

from goods.models import GoodsProfile, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GoodsProfileSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = GoodsProfile
        fields = '__all__'
