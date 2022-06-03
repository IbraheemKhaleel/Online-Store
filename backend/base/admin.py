from django.contrib import admin

# Register your models here.
from base.models import User, Product, PurchaseProduct

admin.site.register(User)
admin.site.register(Product)
admin.site.register(PurchaseProduct)


