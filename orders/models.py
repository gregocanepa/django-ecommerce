from django.db import models
from datetime import datetime


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()


class Order(models.Model):
    date_time = models.DateTimeField(default=datetime.now())

    def get_total(self):
        total_price = 0
        for product_price in Product.objects.filter(orderdetail__order=self):
            total_price += product_price.price
        return total_price


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    product = models.ManyToManyField(Product)

    def total_quantity(self):
        return len(self.products.all())
