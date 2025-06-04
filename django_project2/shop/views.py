from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Category, Product
from django.db.models import Count, F, FloatField, ExpressionWrapper, Avg, Sum

class CategoryListView(ListView):
    model = Category
    template_name = 'shop/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.annotate(product_count=Count('products'))

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'shop/category_detail.html'
    context_object_name = 'category'
    pk_url_kwarg = 'category_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        products = category.products.all().annotate(
            total_value=ExpressionWrapper(F('price') * F('quantity'), output_field=FloatField())
        )
        context['products'] = products
        context['most_expensive'] = products.order_by('-price').first()
        context['cheapest'] = products.order_by('price').first()
        context['average_price'] = products.aggregate(avg_price=Avg('price'))['avg_price'] or 0
        context['total_category_value'] = products.aggregate(
            total_value=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=FloatField()))
        )['total_value'] or 0
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'category', 'price', 'quantity']
    template_name = 'shop/product_form.html'

    def get_success_url(self):
        return reverse_lazy('shop:category_detail', kwargs={'category_id': self.object.category.id})

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'category', 'price', 'quantity']
    template_name = 'shop/product_form.html'
    pk_url_kwarg = 'product_id'

    def get_success_url(self):
        return reverse_lazy('shop:product_detail', kwargs={'product_id': self.object.id})

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'shop/product_confirm_delete.html'
    pk_url_kwarg = 'product_id'

    def get_success_url(self):
        return reverse_lazy('shop:category_detail', kwargs={'category_id': self.object.category.id})
    
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')


    
    