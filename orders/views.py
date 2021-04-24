from .models import Product, Order, OrderDetail
from .serializers import (
    ProductSerializer,
    OrderSerializer,
    OrderDetailSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
import json


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(methods=['get'], detail=False)
    def create_product(self, request, **kwargs):
        """
        Creates a Product. Requires a name and a price.
        """
        product_json = self.request.GET.get('product_json')
        received_json = json.loads(product_json)
        name = received_json.get('name')
        price = received_json.get('price')
        product = Product.objects.create(
            name=name,
            price=price
        )
        product_serializer = ProductSerializer(product).data
        return Response({'New Product Created': product_serializer})

    @action(methods=['get'], detail=False)
    def update_product(self, request, **kwargs):
        """
        Updates a Product. Requires a product pk and can also take
        a name and a price.
        """
        product_json = self.request.GET.get('product_json')
        received_json = json.loads(product_json)
        product_pk = received_json.get('pk')
        name = received_json.get('name')
        price = received_json.get('price')
        product = get_object_or_404(Product, pk=product_pk)
        if name:
            product.name = name
        if price:
            product.price = price
        product.save()
        product_serializer = ProductSerializer(product).data
        return Response({'Product updated': product_serializer})

    @action(methods=['get'], detail=False)
    def delete_product(self, request, **kwargs):
        """
        Deletes a Product. Requires a product pk.
        """
        product_json = self.request.GET.get('product_json')
        received_json = json.loads(product_json)
        product_pk = received_json.get('pk')
        product = get_object_or_404(Product, pk=product_pk)
        product.delete()
        return Response({'Message': f'Product with id {product_pk} deleted'})


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(methods=['get'], detail=False)
    def create_new_order(self, queryset=None, **kwargs):
        """
        Creates a new order. Requires a list of product pks.
        """
        order_request = self.request.GET.get('new_order')
        received_json = json.loads(order_request)
        products = received_json.get('products')
        products = get_list_or_404(Product, pk__in=products)
        total_price = 0
        for product in products:
            total_price = product.price
        new_order = Order.objects.create()
        new_order_detail = OrderDetail.objects.create(
           quantity=len(products),
           price=total_price,
           order=new_order
        )
        new_order_detail.product.add(*products)
        order_serializer = OrderSerializer(new_order).data
        return Response({'New order': order_serializer})

    @action(methods=['get'], detail=False)
    def delete_order(self, request, **kwargs):
        """
        Deletes an Order (an its related OrderDetail).
        Requires an order pk.
        """
        order_json = self.request.GET.get('order_json')
        received_json = json.loads(order_json)
        order_pk = received_json.get('pk')
        order = get_object_or_404(Order, pk=order_pk)
        order.delete()
        return Response({'Message': f'Order with id {order_pk} deleted'})


class OrderDetailViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
