from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt

import json
from web3 import Web3

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

web3.eth.defaultAccount = web3.eth.accounts[0]

abi = json.loads('[{"inputs":[{"internalType":"uint256","name":"_pID","type":"uint256"},{"internalType":"uint256","name":"_uID","type":"uint256"}],"name":"change_owner","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_desc","type":"string"},{"internalType":"uint256","name":"_mID","type":"uint256"},{"internalType":"uint256","name":"_rID","type":"uint256"},{"internalType":"uint256","name":"_oID","type":"uint256"}],"name":"create_product","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"string","name":"_username","type":"string"}],"name":"create_user","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"get_products_count","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"get_users_count","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"productArr","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"description","type":"string"},{"internalType":"uint256","name":"manufactuerID","type":"uint256"},{"internalType":"uint256","name":"retailerID","type":"uint256"},{"internalType":"uint256","name":"ownerID","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"userArr","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"username","type":"string"}],"stateMutability":"view","type":"function"}]')
address = web3.toChecksumAddress("0x83bad3BAe42a184724D05CeB9636dE152fc5753e")

contract = web3.eth.contract(address=address, abi=abi)

# Create your views here.
@csrf_exempt
def signup_view(request):
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            tx_hash = contract.functions.create_user(user.username).transact()
            web3.eth.waitForTransactionReceipt(tx_hash)
            return redirect('smartcontract:list')  
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup_page.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 's@next' in request.POST:
                return redirect(request.POST.get('s@next'))
            else:
                return redirect('smartcontract:list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login_page.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('home')