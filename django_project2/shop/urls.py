from django.urls import path
from .views import (
    CategoryListView, CategoryDetailView, ProductDetailView,
    ProductCreateView, ProductUpdateView, ProductDeleteView
)

app_name = 'shop'

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('category/<int:category_id>/', CategoryDetailView.as_view(), name='category_detail'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='product_add'),
    path('product/<int:product_id>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/<int:product_id>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]

