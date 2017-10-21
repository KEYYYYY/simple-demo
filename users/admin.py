from django.contrib import admin

from .models import UserProfile, VerifyCode


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'mobile', 'add_time')


class VerifyCodeAdmin(admin.ModelAdmin):
    list_display = ('mobile', 'code', 'add_time')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(VerifyCode, VerifyCodeAdmin)
