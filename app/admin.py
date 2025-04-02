from django.contrib import admin
from django.utils.html import format_html
from app.models import *
admin.site.register(Role)
admin.site.register(User)
admin.site.register(product_type)
admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Status)
admin.site.register(Order)