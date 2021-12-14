from django.urls import path
from django.urls import path, include
from home import views 


urlpatterns = [
    path('', views.home, name='home'),
    path('buy', views.buy, name='buy'),
    path('home', views.home, name='Home'),
    path('registration', views.registration, name='registration'),
    path('farmer', views.farmer, name='farmer'),
    path('login', views.user_login, name='login'),
    path('logout', views.logout, name='logout'),
    path('about', views.about, name='about'),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('store', views.store, name="store"),

]
