from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from myapp.models import Product, ProductVariant
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def cart_summary(request):
  cart = Cart(request)
  title = 'Giỏ Hàng'
  cart_products = cart.get_prods
  quantities = cart.get_quants
  totals = cart.cart_total()
  return render( request, 'pages/mains/cart.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'title': title})

def cart_add(request):
  cart = Cart(request)
  if request.POST.get('action') == 'post':
    product_id = int(request.POST.get('product_id'))
    product_qty = int(request.POST.get('product_qty'))
    product_color = request.POST.get('product_color', None)
    product_size = request.POST.get('product_size', None)
    product = get_object_or_404(Product, id = product_id)
    variant = get_object_or_404(ProductVariant, product=product, color=product_color, size=product_size)
    cart.add(variant = variant, quantity = product_qty)
    cart_quantity = cart.__len__()
    response = JsonResponse({'qty': cart_quantity})
    messages.success(request, ("Thêm sản phẩm thành công"))
    return response


def cart_delete(request):
  cart = Cart(request)
  if request.POST.get('action') == 'post':
    variant_id = int(request.POST.get('variant_id'))
    cart.delete(variant=variant_id)
    response = JsonResponse({'variant': variant_id})
    messages.success(request, ("Xóa sản phẩm khỏi giỏ hàng"))
    return response

def cart_update(request):
  cart = Cart(request)
  if request.POST.get('action') == 'post':
    variant_id = int(request.POST.get('variant_id'))
    variant_qty = int(request.POST.get('variant_qty'))
    
    cart.update(variant = variant_id, quantity = variant_qty)
    response = JsonResponse({'qty': variant_qty})
    messages.success(request, ("Cập nhật giỏ hàng thành công"))
    return response