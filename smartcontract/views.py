from django.shortcuts import render, redirect
from .models import Product
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.

def product_list(request):
    products = Product.objects.all().order_by('date')
    return render(request, 'smartcontract/product_list.html', {'products':products})

def product_disp(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'smartcontract/product_display.html', {'product':product})

@login_required(login_url="/accounts/login/")
def product_new(request):
    if request.method == 'POST':
        form = forms.ProductForm(request.POST)
        if form.is_valid():
            s_instance = form.save(commit=False)
            s_instance.manufacturer = request.user
            s_instance.save()
            return redirect('smartcontract:list')
    else:
        form = forms.ProductForm
    return render(request, 'smartcontract/product_create.html', {'form':form})