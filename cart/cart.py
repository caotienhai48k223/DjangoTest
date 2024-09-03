from myapp.models import Product, Profile,ProductVariant
class Cart(): 
  def __init__(self, request):
    self.session = request.session
    self.request = request
    cart = self.session.get('session_key')
    
    if 'session_key' not in request.session:
      cart = self.session['session_key'] = {}
    
    self.cart = cart

  def db_add(self, variant, quantity):
    variant_id = str(variant)
    variant_qty = str(quantity)
    if variant_id in self.cart:
      self.cart[variant_id] += int(variant_qty)
    else:
      self.cart[variant_id] = int(variant_qty)
    self.session.modified = True
    if self.request.user.is_authenticated:
      current_user = Profile.objects.filter(user__id = self.request.user.id)
      carty = str(self.cart)
      carty = carty.replace("\'", "\"")
      current_user.update(old_cart= str(carty))
    

  def add(self, variant, quantity):
    variant_id = str(variant.id)
    variant_qty = str(quantity)
    if variant_id in self.cart:
      self.cart[variant_id] += int(variant_qty)
    else:
      self.cart[variant_id] = int(variant_qty)
    self.session.modified = True
    if self.request.user.is_authenticated:
      current_user = Profile.objects.filter(user__id = self.request.user.id)
      carty = str(self.cart)
      carty = carty.replace("\'", "\"")
      current_user.update(old_cart= str(carty))
    
  def cart_total(self):
    variant_ids = self.cart.keys()
    variants = ProductVariant.objects.filter(id__in=variant_ids)
    quantities = self.cart 
    total = 0
    for key, value in quantities.items():
      key = int(key)
      for variant in variants:
        if variant.id == key:
          if variant.product.is_sale:
            total = total + (variant.product.sale_price * value)
          else:
            total = total + (variant.product.price * value)
    return total
    
  def __len__(self):
    return sum(self.cart.values())
  
  def get_prods(self):
    variant_ids = [int(id) for id in self.cart.keys()]
    variants = ProductVariant.objects.filter(id__in=variant_ids)
    return variants
  
  def get_quants(self):
    quantities = self.cart
    return quantities
  
  def update(self, variant, quantity):
    variant_id = str(variant)
    variant_qty = int(quantity)
    ourcart = self.cart
    ourcart[variant_id] = variant_qty
    self.session.modified = True

    if self.request.user.is_authenticated:
      current_user = Profile.objects.filter(user__id = self.request.user.id)
      carty = str(self.cart)
      carty = carty.replace("\'", "\"")
      current_user.update(old_cart= str(carty))

    thing = self.cart
    return thing
  
  def delete(self, variant):
    variant_id = str(variant)
    if variant_id in self.cart:
      del self.cart[variant_id]
    self.session.modified = True
    if self.request.user.is_authenticated:
      current_user = Profile.objects.filter(user__id = self.request.user.id)
      carty = str(self.cart)
      carty = carty.replace("\'", "\"")
      current_user.update(old_cart= str(carty))
    
    