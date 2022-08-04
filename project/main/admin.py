from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Filter_Price)
admin.site.register(OrderItem)
admin.site.register(Wishlist)



class OrderItemTubelaninline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTubelaninline]

admin.site.register(Order, OrderAdmin)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductTagAdmin(admin.StackedInline):
    model = Tag


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'condition', 'status', 'created_date']
    list_editable = ['condition']
    inlines = [ProductImageAdmin, ProductTagAdmin]
admin.site.register(Product, ProductAdmin)

# admin.site.register(Review)

# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'product', 'rate', 'date_modified']


# admin.site.register(BannerList)
# class BannerListAdmin(admin.ModelAdmin):
#     list_display = ['product', 'title', 'category']

admin.site.register(BannerList)
class BannerListAdmin(admin.ModelAdmin):
    list_display = ['product', 'title', 'category']


admin.site.register(Review)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'rate', 'date_modified']