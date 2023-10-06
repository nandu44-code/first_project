from django.contrib import admin
from . models import Product, VariantImage, Variation
# Register your models here.
admin.site.register(Product)
admin.site.register(Variation)
admin.site.register(VariantImage)
