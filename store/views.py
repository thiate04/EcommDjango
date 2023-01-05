from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
import requests
from .utils import cookieCart, cartData, guestOrder


# Create your views here.
# ///File: store/views.py

def store(request):

     data = cartData(request)
     cartItems = data['cartItems']

     products = Product.objects.all()
     context = {'products':products, 'cartItems':cartItems}
     return render(request, 'store/store.html', context)


# PANIER
def cart(request):

     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'items':items, 'order':order, 'cartItems':cartItems}
     return render(request, 'store/cart.html', context)


# voir produits
def voir(request):

     # data = json.loads(request.body)
     # data = cartData(request)
     # cartItems = data['cartItems']
     # order = data['order']
     # items = data['items']
 
     data = cartData(request)
     cartItems = data['cartItems']
     productId = data['productId']

     products = Product.objects.all()
     product = Product.objects.get(id=productId)
     # orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

     context = {'products':products, 'cartItems':cartItems, 'product':product}
     return render(request, 'store/voir.html', context)
     # context = {'items':items, 'order':order, 'cartItems':cartItems}
     # return render(request, 'store/voir.html', context)

# CONTACT
def contact(request):
     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'items':items, 'order':order, 'cartItems':cartItems}
     return render(request, 'store/contact.html', context)


# CAISSE
def checkout(request):

     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'items':items, 'order':order, 'cartItems':cartItems}
     return render(request, 'store/checkout.html', context)


# MODIFIER ARTICLE
def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']

     print('Action:', action)
     print('ProductId:', productId)


     customer = request.user.customer
     product = Product.objects.get(id=productId)
     order , created = Order.objects.get_or_create(customer=customer, complete=False)

     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

     if action == 'add':
          orderItem.quantity = (orderItem.quantity + 1)
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)

     orderItem.save()

     if orderItem.quantity <= 0:
          orderItem.delete()



     return JsonResponse('Article a été ajouté', safe=False)


def  processOrder(request):
     # print('Donnée:', request.body)
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)
 
     if request.user.is_authenticated:
          customer = request.user.customer
          order , created = Order.objects.get_or_create(customer=customer, complete=False)

         
     else:
        customer, order = guestOrder(request ,data)

     total = float(data['form']['total'])
     order.transaction_id = transaction_id

     if total == order.get_cart_total:
          order.complete = True
     order.save()

     if order.shipping == True:
          ShippingAddress.objects.create(
               customer=customer,
               order=order,
               # numero=data['shipping']['numero'],
               address=data['shipping']['address'],
               city=data['shipping']['city'],
               state=data['shipping']['state'],
               tel=data['shipping']['tel'],
               )

     return JsonResponse('Paiement Complète !', safe=False)



     

# def make_payment(amount, phone_number):
#   headers = {
#     "Authorization": "Bearer YOUR_API_KEY",
#     "Content-Type": "application/json"
#   }
#   data = {
#     "amount": amount,
#     "phoneNumber": phone_number
#   }
#   response = requests.post("https://api.orange.com/payment/v1/payments", headers=headers, json=data)
#   if response.status_code == 201:
#     return response.json()
#   else:
#     return {"error": "An error occurred while processing the payment."}
