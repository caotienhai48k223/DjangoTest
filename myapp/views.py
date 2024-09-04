from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Product, Room, Message, Category, Profile, Collection
from .forms import SignUpForm, UpdateUserForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.db.models import OuterRef, Subquery, Sum
from django.utils.text import slugify
from django.utils import timezone
import json
from cart.cart import Cart
from itertools import chain
from .recently_viewed import RecentlyViewed
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
  title = 'Trang Chủ'
  products= Product.objects.all()
  return render(request, 'pages/index.html', { 'products': products, 'title': title })

def register(request):
  if request.user.is_authenticated:
    return redirect('account')
  else:
    form = SignUpForm()
    title='Đăng Ký'
    if request.method=='POST':
      form = SignUpForm(request.POST)
      if form.is_valid():
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        return redirect('index')
    return render(request, 'pages/accounts/register.html', {'form':form, 'title': title})

def login(request):
  title = 'Đăng Nhập'
  if request.method=="POST":
    username = request.POST['username']
    password = request.POST['password'] 
    user = auth.authenticate(username=username, password=password)
    if user is not None:
      auth.login(request,user)
      
      current_user = Profile.objects.get(user__id =request.user.id)
      save_cart = current_user.old_cart
      if save_cart:
        convert_cart = json.loads(save_cart)
        cart = Cart(request)
        for key, value in convert_cart.items():
          cart.db_add(variant=key, quantity=value)
      return redirect('index')
    else:
      messages.info(request, ' Credential Invalid')
      return redirect('login')
  else:
    return render(request, 'pages/accounts/login.html', {'title': title})

def account(request):
  title = 'Tài Khoản'
  return render(request, 'pages/accounts/account.html', { 'title': title })

def logout(request):
  auth.logout(request)
  return redirect('index')


def update_user(request):
  title = 'Chỉnh Sửa Hồ Sơ'
  if request.user.is_authenticated:
    current_user = User.objects.get(id = request.user.id)
    user_form = UpdateUserForm(request.POST or None, instance=current_user)
    
    if user_form.is_valid():
      user_form.save()
      auth.login(request, current_user)
      messages.success(request, 'Sửa Hồ Sơ Thành Công')
      return redirect('index')
    return render (request, 'pages/accounts/update_user.html', {'title': title, 'user_form': user_form})
  else: 
    return redirect('index')

def update_info(request):
  title = 'Chỉnh Sửa Thông Tin'
  if request.user.is_authenticated:
    current_user = Profile.objects.get(user__id = request.user.id)
    shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
    form = UserInfoForm(request.POST or None, instance=current_user)
    shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    
    if form.is_valid() or shipping_form.is_valid():
      form.save()
      shipping_form.save()
      messages.success(request, 'Sửa Thông Tin Thành Công')
      return redirect('index')
    return render (request, 'pages/accounts/update_info.html', {'title': title, 'form': form , 'shipping_form': shipping_form})
  else: 
    return redirect('index')

def category(request, cat):
  cat = slugify(cat)
  category = Category.objects.filter(slug__icontains=cat).first()
  collection = Collection.objects.filter(slug__icontains=cat).first()
  if category or collection:
    if category:
      products = Product.objects.filter(category=category)
      title = category
    else:
      products = Product.objects.filter(collection=collection)
      title = collection
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price-ascending':
      products = products.order_by('price')
    elif sort_by == 'price-descending':
      products = products.order_by('-price')
    elif sort_by == 'title-ascending':
      products = products.order_by('title')
    elif sort_by == 'title-descending':
      products = products.order_by('-title') 
    elif sort_by == 'created-ascending':
      products = products.order_by('created_date')
    elif sort_by == 'created-descending':
      products = products.order_by('-created_date')
    elif sort_by == 'best-selling':
      products = products.annotate(total_q_purchase=Sum('variants__q_purchase')).order_by('-total_q_purchase')
    else:
      products = products.order_by('?')
    paginator = Paginator(products, 16)
    page_number = request.GET.get('page')
    try:
      page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
      page_obj = paginator.page(1)
    except EmptyPage:
      page_obj = paginator.page(paginator.num_pages)
    return render(request, 'pages/products/category.html', {'page_obj': page_obj, 'title':title, 'sort_by': sort_by})
  else:
    return redirect('collections')


def collections(request):
  title='Tất Cả Sản Phẩm'
  sort_by = request.GET.get('sort_by')
  products= Product.objects.all()
  if sort_by == 'price-ascending':
    products = products.order_by('price')
  elif sort_by == 'price-descending':
    products = products.order_by('-price')
  elif sort_by == 'title-ascending':
    products = products.order_by('title')
  elif sort_by == 'title-descending':
    products = products.order_by('-title') 
  elif sort_by == 'created-ascending':
    products = products.order_by('created_date')
  elif sort_by == 'created-descending':
    products = products.order_by('-created_date')
  elif sort_by == 'best-selling':
    products = products.annotate(total_q_purchase=Sum('variants__q_purchase')).order_by('-total_q_purchase')
  else:
    products = products.order_by('?')
  paginator = Paginator(products, 16)
  page_number = request.GET.get('page')
  try:
    page_obj = paginator.get_page(page_number)
  except PageNotAnInteger:
    page_obj = paginator.page(1)
  except EmptyPage:
    page_obj = paginator.page(paginator.num_pages)
  return render(request, 'pages/products/collections.html', { 'title': title, 'page_obj': page_obj, 'sort_by': sort_by })

def product_detail(request, slug):
  product = get_object_or_404(Product, slug=slug)
  title = product.title
  variants = product.variants.all()
  reviews = product.reviews.all()
  colors = variants.values_list('color', flat=True).distinct()
  sizes = variants.values_list ('size', flat=True).distinct()
  images = list(chain.from_iterable(variants.values_list('image_1', 'image_2', 'image_3', 'image_4').distinct()[::-1]))
  product.images = images
  product.image_main = images[0]
  if None in colors:
    colors = []
  if None in sizes:
    sizes = []
  recommend_list = []
  slug = slug.split('-')
  if 2 < len(slug) < 6:
    slug = slug[2:]
    slug = '-'.join(slug[:2])
    products_recommend = Product.objects.filter(slug__icontains=slug)
    for product_rc in products_recommend:
      if product_rc != product:
        recommend_list.append(product_rc)
    if len(recommend_list) < 6:
      products_category = Product.objects.filter(category=product.category)
      for product_cat in products_category:
        if product_cat != product:
          recommend_list.append(product_cat)   
  else:         
    products_category = Product.objects.filter(category=product.category)
    for product_cat in products_category:
      if product_cat != product and len(recommend_list) < 6:
        recommend_list.append(product_cat)
  recently_viewed = RecentlyViewed(request)
  recently_viewed.add(product.id)
  viewed_products = recently_viewed.get_viewed_products()
  return render(request, 'pages/products/product_detail.html', { 'title': title, 'product': product, 'colors': colors, 'sizes': sizes, 'reviews': reviews, 'recommend_list': recommend_list, 'viewed_products': viewed_products})

def search(request):
  keyword = request.GET.get('keyword', '')
  if keyword:
    title=f"Kết Quả Tìm Kiếm '{keyword}'"
    products = Product.objects.filter(title__icontains=keyword)
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price-ascending':
      products = products.order_by('price')
    elif sort_by == 'price-descending':
      products = products.order_by('-price')
    elif sort_by == 'title-ascending':
      products = products.order_by('title')
    elif sort_by == 'title-descending':
      products = products.order_by('-title') 
    elif sort_by == 'created-ascending':
      products = products.order_by('created_date')
    elif sort_by == 'created-descending':
      products = products.order_by('-created_date')
    elif sort_by == 'best-selling':
      products = products.annotate(total_q_purchase=Sum('variants__q_purchase')).order_by('-total_q_purchase')
    else:
      products = products.order_by('?')
    paginator = Paginator(products, 16)
    page_number = request.GET.get('page')
    try:
      page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
      page_obj = paginator.page(1)
    except EmptyPage:
      page_obj = paginator.page(paginator.num_pages)
    return render(request, 'pages/products/search.html', { 'title': title, 'page_obj': page_obj, 'keyword': keyword, 'sort_by': sort_by })
  else:
    return redirect('collections')




def message_management(request):
  if request.user.is_superuser:
    latest_message_date = Message.objects.filter(room=OuterRef('name')).order_by('-created_date').values('created_date')[:1]
    rooms = Room.objects.filter(name__in=Message.objects.values_list('room', flat=True)).annotate(
        latest_message_date=Subquery(latest_message_date)
    ).order_by('-latest_message_date')
    return render(request, 'pages/messages/mm.html', { 'rooms': rooms })
  else:
    return redirect('index')

def check_box(request):
  name = request.POST['name']
  if Room.objects.filter(name=name).exists():
    return redirect('/account/box-mess/'+ name)
  else:
    new_room = Room.objects.create(name=name)
    new_room.save()
    return redirect('/account/box-mess/'+ name)

def box_mess(request, str):
  room = get_object_or_404(Room, name=str)
  title = room.name
  return render(request, 'pages/messages/box_mess.html', { 'title': title, 'room': room})

def send(request):
  message = request.POST['message']
  username = request.POST['username']
  room_id = request.POST['room_id']
  new_message = Message.objects.create(content=message, user=username, room=room_id, created_date=timezone.now())
  new_message.save()
  return HttpResponse('Gửi tin nhắn thành công')

def getMessages(request, room):
  room = Room.objects.get(name=room)
  messages = Message.objects.filter(room=room.name)
  return JsonResponse({"messages":list(messages.values())})

  