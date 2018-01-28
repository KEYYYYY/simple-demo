from django.contrib import admin

from .models import Goods, Category, UserProfile, Code, GoodsImage


@admin.register(Goods)
class GoodsModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    pass


@admin.register(GoodsImage)
class GoodsImageAdmin(admin.ModelAdmin):
    pass
