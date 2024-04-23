from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Product)
class CartRegister(admin.ModelAdmin):
    list_display = ['id','name','description','category','price','image']
    list_filter = ['category']

@admin.register(Category)
class CategoryRegister(admin.ModelAdmin):
    list_display = ['id','category','gender']
    list_filter = ['gender']

@admin.register(CartItem)
class CartItemView(admin.ModelAdmin):
    list_display = ['id','name','product','price','quantity','total_price']


@admin.register(Recommended)
class RecommendedView(admin.ModelAdmin):
    list_display = ['id','name','gender','price','description','image_1','image_2','image_3','image_4']