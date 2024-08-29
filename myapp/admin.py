from django.contrib import admin
from .models import Product, Message, Room, Order, Category, Customer, Profile, ProductVariant
from django.utils.html import format_html
from django.contrib.auth.models import User

# Register your models here.
class ProductVariantInline(admin.TabularInline):
  model = ProductVariant
  extra = 1  # Số lượng form biến thể trống sẽ hiển thị thêm khi tạo mới
  
class ProductAdmin(admin.ModelAdmin):
  list_display = ('title', 'category', 'image_preview', 'price')
  inlines = [ProductVariantInline]
  search_fields = ('title', 'category__name')
  prepopulated_fields = {'slug': ('title',)}
  list_filter = ('category', 'is_sale', 'created_date')
  def image_preview(self, obj):
      if obj.thumbnail:
        return format_html('<img src="{}" width="50" height="auto" />'.format(obj.thumbnail))
      return "No Image"
  image_preview.short_description = 'Image Preview'
  
  
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
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

