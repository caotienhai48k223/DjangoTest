from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from myapp.models import Product
# Create your views here.
def checkout(request):
  title = 'Thanh Toán'
  cart = Cart(request)
  cart_products = cart.get_prods
  quantities = cart.get_quants
  totals = cart.cart_total()
  if request.user.is_authenticated:
    shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
    shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    return render(request, 'pages/payments/checkout.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form, 'title': title})
  else:
    shipping_form = ShippingForm(request.POST or None)
    return render(request, 'pages/payments/checkout.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form, 'title': title})

def billing_info(request):
  if request.POST:
    cart = Cart(request)
    title = 'Thông Tin Đơn Hàng'
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    my_shipping = request.POST
    request.session['my_shipping'] = my_shipping
    if request.user.is_authenticated:
      billing_form = PaymentForm()
      return render(request, 'pages/payments/billing_info.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_info': request.POST, 'billing_form': billing_form, 'title': title})
    else:
      billing_form = PaymentForm()
      return render(request, 'pages/payments/billing_info.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_info': request.POST, 'billing_form': billing_form, 'title': title})
  else:
    return redirect('index')

def process_order(request):
  if request.POST:
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    payment_form = PaymentForm(request.POST or None)
    my_shipping = request.session.get('my_shipping')
    full_name = my_shipping['shipping_full_name']
    email = my_shipping['shipping_email']
    shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}"
    amount_paid = totals
    
    if request.user.is_authenticated:
      user = request.user 
      create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
      create_order.save()
      order_id = create_order.pk
      for item in cart_products():
        variant_id = item.id
        if item.product.is_sale:
          price = item.product.sale_price
        else:
          price = item.product.price
        for key, value in quantities().items():
          if int(key) == variant_id:
            create_order_item = OrderItem(order_id=order_id, product_variant_id=variant_id, user=user, quantity=value, price=price )
            create_order_item.save()
      for key in list(request.session.keys()):
        if key == "session_key":
          del request.session[key]
      messages.success(request, 'Đặt Hàng Thành Công')
      return redirect('index')
    else:
      create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
      create_order.save()
      order_id = create_order.pk
      for item in cart_products():
        variant_id = item.id
        if item.product.is_sale:
          price = item.product.sale_price
        else:
          price = item.product.price
        for key, value in quantities().items():
          if int(key) == variant_id:
            create_order_item = OrderItem(order_id=order_id, product_variant_id=variant_id, quantity=value, price=price )
            create_order_item.save()
      for key in list(request.session.keys()):
        if key == "session_key":
          del request.session[key]
      messages.success(request, 'Đặt Hàng Thành Công')
      return redirect('index')
  else:
    return redirect('index')

def payment_success(request):
  return render(request, 'payments/payments/payment_success.html')
