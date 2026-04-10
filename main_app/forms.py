from django import forms
from .models import Product, Category, Order, CartItem, Blogpost

# ------------------------
# CATEGORY FORM
# ------------------------
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter category name'
            }),
        }


# ------------------------
# PRODUCT FORM
# ------------------------
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'stock', 'image', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Enter product description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': '0.00'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control', 
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ------------------------
# ORDER FORM (FOR ADDRESS)
# ------------------------
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address']
        widgets = {
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter delivery address'
            }),
        }


# ------------------------
# CART ITEM QUANTITY UPDATE
# ------------------------
class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            })
        }



# ------------------------
# Blog Post
# ------------------------
class Blogform(forms.ModelForm):
    class Meta:
        model = Blogpost
        field = ['title', 'category', 'body']