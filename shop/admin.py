from django.contrib import admin

# Register your models here.
from shop.models import Shop, Receipt, Product, ProductsReceipt


admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Receipt)
admin.site.register(ProductsReceipt)