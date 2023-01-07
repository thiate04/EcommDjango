# ///File: store/urls.py

from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	# path('voir/', views.voir, name="voir"),
	path('<int:myid>', views.voir, name="voir"),
	path('contact/', views.contact, name="contact"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

]