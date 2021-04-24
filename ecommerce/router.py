from orders.views import ProductViewSet, OrderViewSet, OrderDetailViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register('products', ProductViewSet)
router.register('orders', OrderViewSet)
router.register('orders_details', OrderDetailViewSet)

for url in router.urls:
    print(url)