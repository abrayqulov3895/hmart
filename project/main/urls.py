from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('', home, name='home'),
    path('search/', views.search, name='search'),
    path('about/', about, name='about'),
    path('cart/', cart, name='cart'),
    path('wishlist/', wishlist, name='wishlist'),
    path('account/', account, name='account'),
    path('shop/', shop, name='shop'),
    path('product_slider/', product_slider, name='product_slider'),
    path('product_detail/<int:id>/', views.product_detail, name='product_detail'),
    path('category_detail/<int:id>/', views.category_detail, name='category_detail'),
    path('color_detail/<int:id>/', views.color_detail, name='color_detail'),
    path('price_detail/<int:id>/', views.price_detail, name='price_detail'),
    path('brand_detail/<int:id>/', views.brand_detail, name='brand_detail'),
    path('blog/', blog, name='blog'),
    path('blog_single/', blog_single, name='blog_single'),
    path('contact', contact, name='contact'),
    path('item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart_add/<int:id>/', views.cart_add, name='cart_add'),
    path('item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart_detail/',views.cart_detail,name='cart_detail'),
    path('empty_cart/', views.empty_cart, name='empty_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('create-checkout-session/', CreateCheckoutView.as_view(), name="create-checkout-session")
]
