from .models import Product, Profile

class RecentlyViewed():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        recently_viewed = self.session.get('recently_viewed', [])
        
        self.recently_viewed = recently_viewed

    def add(self, product_id):
        product_id = int(product_id)
        if product_id not in self.recently_viewed:
            self.recently_viewed.append(product_id)
            if len(self.recently_viewed) > 10:
                self.recently_viewed.pop(0)
        
        if self.request.user.is_authenticated:
            current_user = Profile.objects.get(user__id=self.request.user.id)
            profile_viewed = current_user.recently_viewed or []
            combined_viewed = list(dict.fromkeys(profile_viewed + self.recently_viewed))[:10]  
            current_user.recently_viewed = combined_viewed
            current_user.save()
            
            self.session['recently_viewed'] = combined_viewed
        else:
            self.session['recently_viewed'] = self.recently_viewed
        self.session.modified = True
        
        
    def get_viewed_products(self):
        product_ids = [int(id) for id in self.recently_viewed]
        products = Product.objects.filter(id__in=product_ids)
        return products