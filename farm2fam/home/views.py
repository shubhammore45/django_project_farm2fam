from django.contrib.auth import forms
from django.shortcuts import render,redirect
from django.contrib import messages
from home.models import  Farmer, Product
from .forms import CustomUserForm  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder

# Create your views here.


def home(request):
    return render(request, ('home.html'))


def buy(request):
    return render(request, ('buy.html'))


def registration(request):
    if request.method == 'POST':
        fm=CustomUserForm(request.POST or None)
        if fm.is_valid():
            fm.save()
        return render(request, 'login.html',{'form':fm})
    else:
        fm=CustomUserForm()
        return render(request, 'registration.html',{'form':fm})

def farmer(request):
    if request.method == 'POST':
        name = request.POST.get('farmer_name')
        phone = request.POST.get('contact_no')
        email=request.POST.get('farmer_email')
        address = request.POST.get('address')
        product = request.POST.get('sku')
        town = request.POST.get('town')
        district = request.POST.get('district')
        pincode = request.POST.get('pincode')
        farmer = Farmer(name=name, phone=phone,email=email, address=address,
                        product=product, town=town, district=district, pincode=pincode)
        farmer.save()
        messages.success(request, 'Your form is Submitted!')

    return render(request, ('farmer.html'))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'Try again! username or password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login.html')


@login_required(login_url='login')
def home_page(request):
    return render(request, 'home.html')

def about(request):
    return render(request, ('about.html'))

def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'cart.html', context)

def checkout(request):
    data = cartData(request)
	
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
	
    if action == 'add':
    	orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
    	orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
    	orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)