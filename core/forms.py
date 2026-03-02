from django import forms
from .models import Product, Category, Sale,Expense , Customer ,Staff ,Supplier, Invoice, InvoiceItem
from django.core.exceptions import ValidationError
import re


# 1. Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
        }



# 2. Product Form (Fixed: uses image_url instead of image)
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'stock_quantity', 'image_url']  # <--- Changed to image_url
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Paste Image Link Here'}),
        }



# 3. Sale Form (New!)
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Quantity'}),
        }



# 4. Expense Form
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'category', 'amount', 'date_added']
        widgets = {
            'date_added': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Shop Rent'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        }



# 5. Customer form
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number', 'pattern': '[0-9]{10}', 'maxlength': '10', 'minlength': '10', 'title': 'Please enter exactly 10 digits'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Address'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if len(phone) != 10:
                raise ValidationError("Phone number must be exactly 10 digits.")
            if not phone.isdigit():
                raise ValidationError("Phone number must contain only numbers.")
            if phone.startswith('0'):
                raise ValidationError("Phone number cannot start with 0.")

        return phone


# 6. staff salary 
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'position','email', 'phone', 'salary']



#7. supplier
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company_name', 'contact_person', 'phone', 'email', 'address']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Person'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (Optional)'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone:
            if len(phone) != 10:
                raise ValidationError("Phone number must be exactly 10 digits.")
            if not phone.isdigit():
                raise ValidationError("Phone number must contain only numbers.")
            if phone.startswith('0'):
                raise ValidationError("Phone number cannot start with 0.")

        return phone



# 8. Invoice Forms
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
        }

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
        }