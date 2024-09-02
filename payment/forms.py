from django import forms
from .models import ShippingAddress
from myapp.models import ProductReview

class ShippingForm(forms.ModelForm):
  PAYMENT_CHOICES = [('cash', 'Thanh Toán Khi Nhận Hàng'), ('card', 'Thanh Toán Chuyển Khoản Ngân Hàng'),]
  shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Họ Tên'}), required=True)
  shipping_phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Số Điện Thoại'}), required=True)
  shipping_address = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Địa Chỉ'}), required=True)
  shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Thành Phố'}), required=True)
  shipping_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Tỉnh'}), required=True)
  shipping_payment_type = forms.ChoiceField(label="", choices=PAYMENT_CHOICES, widget=forms.RadioSelect(attrs={'id':'payment-type'}), initial='cash', required=False)
  shipping_card_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'id':'card-form', 'placeholder': 'Số Thẻ'}), required=False)
  shipping_bank = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'id':'card-form', 'placeholder': 'Tên Ngân Hàng'}), required=False)
  
  class Meta: 
    model = ShippingAddress
    fields = ['shipping_full_name', 'shipping_phone', 'shipping_address', 'shipping_city', 'shipping_state', 'shipping_payment_type', 'shipping_card_number', 'shipping_bank']
    exclude = ['user', ]
    
class ProductReviewForm(forms.ModelForm):
  STAR_CHOICES = [('1', '⭐'), ('2', '⭐⭐'), ('3', '⭐⭐⭐'), ('4', '⭐⭐⭐⭐'), ('5', '⭐⭐⭐⭐⭐')]
  rating = forms.ChoiceField(label="Đánh Giá", choices=STAR_CHOICES, widget=forms.Select(attrs={'id': 'star-review', 'class':'form-select text-center'}), initial='5', required=True)
  content = forms.CharField(label='Bình Luận', widget=forms.Textarea(attrs={'class':'form-control'}), required=True)
  
  class Meta:
    model = ProductReview
    fields = ['rating', 'content']
