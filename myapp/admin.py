from django.contrib import admin
from .models import Product, Message, Room, Category, Profile, ProductVariant, ProductReview, Collection
from django.contrib.auth.models import User

# Register your models here.
class ProductVariantInline(admin.TabularInline):
  model = ProductVariant
  extra = 1  

class ProductReviewInline(admin.TabularInline):
  model = ProductReview
  extra = 0

class ProductAdmin(admin.ModelAdmin):
  list_display = ('title', 'category', 'price')
  inlines = [ProductVariantInline,  ProductReviewInline]
  prepopulated_fields = {'slug': ('title',)}
  list_filter = ('category', 'is_sale', 'created_date')
  
  
admin.site.register(Category)
admin.site.register(Collection)
admin.site.register(Product, ProductAdmin)
admin.site.register(Profile)
admin.site.register(Room)
admin.site.register(Message)

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    filed = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]
    list_display = ('username', 'first_name', 'last_name', 'staff_status')
    def staff_status(self, obj):
        return obj.is_staff
    staff_status.boolean = True
    staff_status.short_description = 'Staff Status'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

