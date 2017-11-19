import xadmin

from goods.models import GoodsProfile


class GoodsProfileAdmin:
    list_display = ['name', 'price', 'add_time']
    search_fields = ['name', 'price', 'add_time']
    list_filter = ['name', 'price', 'add_time']


xadmin.site.register(GoodsProfile, GoodsProfileAdmin)
