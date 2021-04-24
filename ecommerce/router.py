from orders.views import ProductViewSet, OrderViewSet, OrderDetailViewSet
from rest_framework import routers
from django.urls import resolve

router = routers.DefaultRouter()

router.register('products', ProductViewSet, basename='product')
router.register('orders', OrderViewSet, basename='order')
router.register('orders_details', OrderDetailViewSet, basename='order_detail')

for url in router.urls:
    print(url)