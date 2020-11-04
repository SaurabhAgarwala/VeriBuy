from django.shortcuts import render, redirect
from .models import Product
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from . import forms

import json
from web3 import Web3

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

web3.eth.defaultAccount = web3.eth.accounts[0]

abi = json.loads('[{"inputs":[{"internalType":"uint256","name":"_pID","type":"uint256"},{"internalType":"uint256","name":"_uID","type":"uint256"}],"name":"change_owner","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_desc","type":"string"},{"internalType":"uint256","name":"_mID","type":"uint256"},{"internalType":"uint256","name":"_rID","type":"uint256"},{"internalType":"uint256","name":"_oID","type":"uint256"}],"name":"create_product","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"string","name":"_username","type":"string"}],"name":"create_user","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"get_products_count","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"get_users_count","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"productArr","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"description","type":"string"},{"internalType":"uint256","name":"manufactuerID","type":"uint256"},{"internalType":"uint256","name":"retailerID","type":"uint256"},{"internalType":"uint256","name":"ownerID","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"userArr","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"username","type":"string"}],"stateMutability":"view","type":"function"}]')
address = web3.toChecksumAddress("0x83bad3BAe42a184724D05CeB9636dE152fc5753e")

contract = web3.eth.contract(address=address, abi=abi)

# Create your views here.

def home(request):
    return render(request, 'smartcontract/index.html')

def product_list(request):
    products = get_products_frm_contract()
    for product in products:
        for i in range(3,6):
            product[i] = contract.functions.userArr(product[i]).call()[1]
    return render(request, 'smartcontract/product_list.html', {'products':products})

def get_products_frm_contract():
    func_to_call = 'get_products_count'
    contract_func = contract.functions[func_to_call]
    product_count = contract_func().call()

    products = []
    for i in range(product_count):
        product = contract.functions.productArr(i+1).call()
        products.append(product)
    return products

def product_disp(request, id):
    product = contract.functions.productArr(int(id)).call()
    for i in range(3,6):
        product[i] = contract.functions.userArr(product[i]).call()[1]
    return render(request, 'smartcontract/product_display.html', {'product':product})

@csrf_exempt
@login_required(login_url="/accounts/login/")
def product_new(request):
    if request.method == 'POST':
        form = forms.ProductForm(request.POST)
        if form.is_valid():
            tx_hash = contract.functions.create_product(form.cleaned_data["name"], form.cleaned_data["desc"], request.user.id, form.cleaned_data["retailer"].id, form.cleaned_data["retailer"].id).transact()
            web3.eth.waitForTransactionReceipt(tx_hash)
            return redirect('smartcontract:list')
    else:
        form = forms.ProductForm
    return render(request, 'smartcontract/product_create.html', {'form':form})

@csrf_exempt
@login_required(login_url="/accounts/login/")
def change_owner(request, id):
    if request.method == "POST":
        form = forms.EditOwnerForm(request.POST)
        if form.is_valid():
            tx_hash = contract.functions.change_owner(int(id),form.cleaned_data["owner"].id).transact()
            web3.eth.waitForTransactionReceipt(tx_hash)
            return redirect('smartcontract:list')
    else:
        product = contract.functions.productArr(int(id)).call()
        for i in range(3,6):
            product[i] = contract.functions.userArr(product[i]).call()[1]
        form = forms.EditOwnerForm()
        return render(
            request, "smartcontract/transfer_ownership.html", {'form':form, 'product': product}
        )
