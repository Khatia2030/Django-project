from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # ჩანაწერთა სიის ველების ჩვენება

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity')
    list_filter = ('category',)  # ფილტრი კატეგორიით
    search_fields = ('name',)    # ძებნა სახელითrom django.contrib import admin

# Register your models here.