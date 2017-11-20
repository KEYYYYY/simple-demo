import django_filters

from goods.models import GoodsProfile


class GoodsProfileFilter(django_filters.rest_framework.FilterSet):
    """
    商品过滤器
    """
    price_min = django_filters.NumberFilter(name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(name='price', lookup_expr='lte')
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta:
        model = GoodsProfile
        fields = ['name', 'category', 'price_min', 'price_max']
