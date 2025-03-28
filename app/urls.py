# app/urls.py

from django.urls import path
from .views import *
from django.contrib import admin
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()

# router.register('users', UserViewSet, basename='users')
# router.register('group', GroupViewSet, 'view_group')
router.register('products', ProductView, basename='products')
router.register('orders', OrderView, basename='orders')
router.register('order-status', OrderStatusView, basename='order-status')
router.register('order-details', OrderDetailView, basename='order-details')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
