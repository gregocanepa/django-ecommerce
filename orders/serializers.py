from rest_framework import serializers
from .models import Product, Order, OrderDetail


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('__all__')


class OrderDetailSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()

    basket = ProductSerializer(
        source='product',
        many=True,
        read_only=True
    )

    class Meta:
        model = OrderDetail
        fields = [
            'pk',
            'basket',
            'quantity'
        ]

    def get_quantity(self, obj):
        return len(obj.product.all())


class OrderSerializer(serializers.ModelSerializer):
    total_sum = serializers.SerializerMethodField()

    order_detail = OrderDetailSerializer(
        source='orderdetail_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            'pk',
            'order_detail',
            'total_sum',
            'date_time'
        ]

    def get_total_sum(self, obj):
        return obj.get_total()
