from django.urls import path
from . import views

urlpatterns = [
  path('payment_success/', views.payment_success, name='payment-success'),
  path('checkout/', views.checkout, name='checkout'),
  path('billing_info/', views.billing_info, name = 'billing-info'),
  path('process_order/', views.process_order, name='process-order'),
  path('shipped_tab/', views.shipped_tab, name='shipped-tab'),
  path('unshipped_tab/', views.unshipped_tab, name='unshipped-tab'),
  path('order/<int:pk>/', views.order, name='order')
]