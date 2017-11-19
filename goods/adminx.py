import xadmin

from goods.models import GoodsProfile, Category


class GoodsProfileAdmin:
    list_display = ['name', 'price', 'category', 'add_time']
    search_fields = ['name', 'price', 'category', 'add_time']
    list_filter = ['name', 'price', 'category', 'add_time']


class CategoryAdmin:
    list_display = ['name', 'add_time']
    search_fields = ['name', 'add_time']
    list_filter = ['name', 'add_time']


xadmin.site.register(GoodsProfile, GoodsProfileAdmin)
xadmin.site.register(Category, CategoryAdmin)
