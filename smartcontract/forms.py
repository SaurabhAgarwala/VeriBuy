from django import forms
from . import models

class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['name', 'desc', 'retailer']

class EditOwnerForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['owner']

