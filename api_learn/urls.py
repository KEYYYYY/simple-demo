"""api_learn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from rest_learn import views

router = DefaultRouter()
router.register('goods', views.GoodsViewSet)
router.register('categorys', views.CategoryViewSet)
router.register('codes', views.CodeViewSet, base_name='codes')
router.register('users', views.UserViewSet, base_name='users')
router.register('users-fav', views.UserFavViewSet, base_name='users-fav')
router.register('banners', views.BannerViewSet)
router.register(
    'users-shopping', views.ShoppingCartViewSet, base_name='users-shopping'
)
router.register(
    'users-address', views.AddressViewSet, base_name='users-address'
)
router.register(
    'users-orders', views.OrderViewSet, base_name='users-orders'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', include_docs_urls(title='测试')),
    path('login/', obtain_jwt_token),
    path('', include(router.urls)),
]
