from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
  shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Họ Tên'}), required=True)
  shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Địa Chỉ Email'}), required=True)
  shipping_address = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Địa Chỉ'}), required=True)
  shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Thành Phố'}), required=True)
  shipping_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Tỉnh'}), required=True)
  
  class Meta: 
    model = ShippingAddress
    fields = ['shipping_full_name', 'shipping_email', 'shipping_address', 'shipping_city', 'shipping_state']
    
    exclude = ['user', ]
    
class PaymentForm(forms.Form):
  cart_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Số Tài Khoản'}), required=True)
  bank_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Tên Ngân Hàng'}), required=True)