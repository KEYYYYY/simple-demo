from django_filters import rest_framework as filters

from .models import Goods


class GoodsFilter(filters.FilterSet):
    class Meta:
        model = Goods
        fields = {
            'category': ['exact'],
            'price': ['exact', 'gte', 'lte'],
            'add_time': [
                'exact', 'year__gte', 'year__lte', 'month__gte', 'month__lte',
                'day__lte', 'day__gte',
            ]
        }
