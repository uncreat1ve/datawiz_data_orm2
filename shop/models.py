from __future__ import unicode_literals
from django.db import models
from django_pandas.managers import DataFrameManager

class Shop(models.Model):
    shop_name = models.CharField(max_length=200)

    objects = DataFrameManager()


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    objects = DataFrameManager()


class Receipt(models.Model):
    receipt_date = models.DateTimeField()
    receipt_items_qty = models.IntegerField()
    receipt_week_day = models.IntegerField()
    receipt_total_price = models.FloatField()
    receipt_shop = models.ForeignKey(Shop)
    objects = DataFrameManager()


class ProductsReceipt(models.Model):
    receipt = models.ForeignKey(Receipt)
    order_no = models.IntegerField()
    product = models.ForeignKey(Product)
    qty = models.FloatField()
    price = models.FloatField()
    objects = DataFrameManager()
# Create your models here.
