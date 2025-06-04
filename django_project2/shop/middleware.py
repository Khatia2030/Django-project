import time
from django.utils.deprecation import MiddlewareMixin
from shop.models import Product

class ProductAccessAndTimingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_view(self, request, view_func, view_args, view_kwargs):
        # თუ მიდის კონკრეტულ პროდუქტზე
        if view_func.__name__ == 'ProductDetailView':
            product_id = view_kwargs.get('product_id')
            if product_id:
                try:
                    product = Product.objects.get(pk=product_id)
                    product.views = (product.views or 0) + 1
                    product.save(update_fields=['views'])
                except Product.DoesNotExist:
                    pass

    def process_response(self, request, response):
        duration = time.time() - getattr(request, 'start_time', time.time())
        print(f"[Middleware] Request duration: {duration:.4f} წამი")
        return response