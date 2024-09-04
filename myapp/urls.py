from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('register/', views.register, name='register'),
  path('login/', views.login, name='login'),
  path('account/', views.account, name='account'),
  path('update_user/', views.update_user, name = 'update-user'), 
  path('update_info/', views.update_info, name = 'update-info'), 
  path('logout/', views.logout, name='logout'),
  path('collections/', views.collections, name='collections'),
  path('products/', views.collections, name='collections'),
  path('collections/tat-ca-san-pham/', views.collections, name='collections'),
  path('collections/all/', views.collections, name='collections'),
  path('collections/<str:cat>/', views.category, name='collections-category'),
  path('products/<slug:slug>/', views.product_detail, name='product-detail'),
  path('search/', views.search, name='search'),
  path('message-management/', views.message_management, name='message-management'),
  path('account/box-mess/check-box', views.check_box, name='check-box'),
  path('account/box-mess/send', views.send, name='send'),
  path('account/box-mess/getMessages/<str:room>/', views.getMessages, name='getMessages'),
  path('account/box-mess/<str:str>', views.box_mess, name='box-mess')
]