"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

import xadmin
from app import settings
from goods.views import CategoryViewSet, GoodsProfileViewSet
from users.views import LoginView

router = DefaultRouter()

# 配置GoodsProfile的url
router.register(r'goods', GoodsProfileViewSet)
router.register(r'categorys', CategoryViewSet)

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(
        r'^media/(?P<path>.*)$',
        serve,
        {'document_root': settings.MEDIA_ROOT}
    ),
    # Rest登陆url
    url(
        r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    # 获取token的url
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^', include(router.urls)),
    url(r'^login/', LoginView.as_view(), name='login'),
]
