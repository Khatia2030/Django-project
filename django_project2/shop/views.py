from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.db.models import Count, Max, Min, Avg, F, FloatField, ExpressionWrapper, Sum

def category_list(request):
    categories = Category.objects.annotate(product_count=Count('products'))
    return render(request, 'shop/category_list.html', {'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()

    # ჯამური ღირებულება თითოეულ პროდუქტზე (price * quantity)
    # უკვე გვაქვს მეთოდი product.total_value(), მაგრამ აქ აგრეგაციისთვის:
    products_with_total = products.annotate(
        total_value=ExpressionWrapper(F('price') * F('quantity'), output_field=FloatField())
    )

    # სტატისტიკა
    most_expensive = products.order_by('-price').first()
    cheapest = products.order_by('price').first()
    average_price = products.aggregate(avg_price=Avg('price'))['avg_price'] or 0
    total_category_value = products.aggregate(
        total_value=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=FloatField()))
    )['total_value'] or 0

    context = {
        'category': category,
        'products': products_with_total,
        'most_expensive': most_expensive,
        'cheapest': cheapest,
        'average_price': average_price,
        'total_category_value': total_category_value,
    }
    return render(request, 'shop/category_detail.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

from .forms import ProductForm
from django.shortcuts import redirect

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop:category_list')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})