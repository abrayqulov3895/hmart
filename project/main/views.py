from http import client
from itertools import product
from math import prod, remainder
from multiprocessing.sharedctypes import Value
from unicodedata import category
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.db.models import Min, Max
from django.views import View
from django.conf import settings
from django.views.generic import TemplateView
import stripe
from .forms import *
# import razorpay

stripe.api_key = settings.STRIPE_SECRET_KEY



# Create your views here.


def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken. ')
            return HttpResponseRedirect(request.path_info)
        
        user_obj = User.objects.create(username=username, email=email, password=password)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'An email has been sent on your mail. ')
        return HttpResponseRedirect(request.path_info)




    return render(request, 'register.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')



def home(request):
    products = Product.objects.filter(status='Publish', condition='New').order_by('-created_date')
    bannerlists = BannerList.objects.all()
    categories = Category.objects.all()
    print(categories.values)
    print(categories)
    cheapests = Product.objects.all() 
    lowest_price = cheapests.aggregate(Min('price'))
    lowest_products = Product.objects.filter(price=lowest_price["price__min"])

    price_min = lowest_price["price__min"]

    if request.user.is_authenticated:
        wish_list = Wishlist.objects.filter(user = request.user)
    else:
        wish_list = []
    
    if request.method == "POST" and request.user.is_authenticated:
        user = request.user
        product = Product.objects.get(id = request.POST.get('product_id'))

        try:
            wishlist = Wishlist.objects.get(user=user,product= product)
            wishlist.delete()
        
        except:
            Wishlist.objects.create(user = user, product=product)

        



    context = {
        'products':products,
        'bannerlists':bannerlists,
        'cheapests':cheapests,
        'lowest_products':lowest_products,
        'price_min':price_min,
        'wish_list':wish_list
    }
    return render(request, 'home.html', context)

def search(request):
    q = request.GET['q']
    products = Product.objects.filter(name__icontains = q).order_by('-created_date')
    print(q)
    context = {
        'products':products,

    }
    return render(request, 'search.html', context)

def about(request):
    return render(request, 'about.html')
def account(request):
    return render(request, 'account.html')
def blog(request):
    return render(request, 'blog.html')
def blog_single(request):
    return render(request, 'blog-single.html')
def cart(request):
    return render(request, 'cart.html')
def contact(request):
    return render(request, 'contact.html')
def product_slider(request):
    return render(request, 'product-slider.html')
def wishlist(request):
    if request.user.is_authenticated:
        wish_list = Wishlist.objects.filter(user = request.user)
        context = {
            'wish_list':wish_list,
        }
          
    if request.method == "POST" and request.user.is_authenticated and request.POST.get('count'):
            print(request.POST)
    if request.method == "POST" and request.user.is_authenticated and  not request.POST.get('count'):
        print('post')
        user = request.user
        product  = Product.objects.get(id= request.POST.get('product_id'))
        
        try:
            wishlist = Wishlist.objects.get(user=user, product=product)
            wishlist.delete()
            print(wishlist)    

        except:
            Wishlist.objects.create(user=user, product=product)
    return render(request, 'wishlist.html',context)
def shop(request):
    products = Product.objects.filter(status='Publish').order_by('-created_date')
    categories = Category.objects.all()
    filter_prices = Filter_Price.objects.all()
    colors = Color.objects.all()
    brands = Brand.objects.all()
    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')
    PLTOHID = request.GET.get('PLTOH')
    HTOLID = request.GET.get('HTOL')
    NEWID = request.GET.get('NEW')
    OLDID = request.GET.get('OLD')



    if ATOZID:
        products = Product.objects.filter(status='Publish').order_by('name')
    elif ZTOAID:
        products = Product.objects.filter(status='Publish').order_by('-name')
    elif PLTOHID:
        products = Product.objects.filter(status='Publish').order_by('price')
    elif HTOLID:
        products = Product.objects.filter(status='Publish').order_by('-price')
    elif NEWID:
        products = Product.objects.filter(status='Publish', condition='New')
    elif OLDID:
        products = Product.objects.filter(status='Publish', condition='Old')

    
    
    
    




    context = {
        'products':products,
        'categories':categories,
        'filter_prices':filter_prices,
        'colors':colors,
        'brands':brands
    }
    return render(request, 'shop.html', context)


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)[:4]



    reviews = Review.objects.filter(product=product).order_by('-date_modified')
    if request.method == "GET":
        review_form = ReviewForm(request.GET or None)
        if review_form.is_valid():
            # prod_id = request.GET.get('prod_id')
            # product = Product.objects.get(id=prod_id)
            comment = request.GET.get('comment')
            rate = request.GET.get('rate')
            user = request.user

            review = Review.objects.create(product=product, user=request.user, comment=comment, rate=rate)
            review.save()
            return redirect('product_detail', product.id)
    else:
        review_form = ReviewForm()
    


    context = {
        'product':product,
        'reviews':reviews,
        'related_products':related_products,
    }

    return render(request, 'product_detail.html', context)

def color_detail(request, id):
    categories = Category.objects.all()
    filter_prices = Filter_Price.objects.all()
    brands = Brand.objects.all()

    color = get_object_or_404(Color, id=id)

    colors = Color.objects.all()
    products = color.productcolor.filter(status='Publish').order_by('-created_date')
    




    context = {
        'products':products,
        'categories':categories,
        'filter_prices':filter_prices,
        'colors':colors,
        'brands':brands
    }



    return render(request, 'color_detail.html', context)


def category_detail(request, id):
    filter_prices = Filter_Price.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()
    category = get_object_or_404(Category, id=id)
    categories = Category.objects.all()
    products = category.productcategory.filter(status='Publish').order_by('-created_date')
    cheapests = Product.objects.all() 
    lowest_price = cheapests.aggregate(Min('price'))
    lowest_products = category.productcategory.filter(price=lowest_price["price__min"])
    




    context = {
        'products':products,
        'categories':categories,
        'filter_prices':filter_prices,
        'colors':colors,
        'brands':brands,
        'category':category,
        'lowest_products':lowest_products
    }



    return render(request, 'category_detail.html', context)


def price_detail(request, id):
    filter_prices = Filter_Price.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()
    categories = Category.objects.all()
    price = get_object_or_404(Filter_Price, id=id)
    products = price.productpricefilter.filter(status='Publish').order_by('-created_date')
    




    context = {
        'products':products,
        'categories':categories,
        'filter_prices':filter_prices,
        'colors':colors,
        'brands':brands,
        'price':price
    }



    return render(request, 'price_detail.html', context)


def brand_detail(request, id):
    filter_prices = Filter_Price.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()
    categories = Category.objects.all()
    brand = get_object_or_404(Brand, id=id)
    products = brand.productbrand.filter(status='Publish').order_by('-created_date')
    




    context = {
        'products':products,
        'categories':categories,
        'filter_prices':filter_prices,
        'colors':colors,
        'brands':brands,
        'brand':brand
    }



    return render(request, 'brand_detail.html', context)



# -------------------------------------------CART FUNCTION ----------------------------------------


@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    messages.info(request, 'This product was added to your cart.')
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    messages.info(request, 'This product remove to your cart.')
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    messages.info(request, 'This product again added to your cart.')
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    messages.info(request, 'This product one remove to your cart.')
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, 'Your cart full remove.')
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')

@login_required(login_url="/login/")



def checkout(request):
    payment = Checkout.objects.create(
        user=request.user
    )

    print(payment)

    return render(request, 'cart/checkout.html')

def place_order(request):
    if request.method == "POST":
        first_name = request.POST.get('firstname')
        # last_name = request.POST.get('lastname')
        # firs_name = request.POST.get('firstname')
        # firs_name = request.POST.get('firstname')
        # firs_name = request.POST.get('firstname')
        # firs_name = request.POST.get('firstname')
        # firs_name = request.POST.get('firstname')
        # firs_name = request.POST.get('firstname')
        # firs_name = request.POST.get('firstname')
        # firs_name = request.POST.get('firstname')
        # firs_name = request.POST.get('firstname')

        print(first_name)

    return render(request, 'cart/placeorder.html')


def empty_cart(request):
    return render(request, 'cart/empty_cart.html')



class CreateCheckoutView(View):
    def product(self, *args, **kwargs):
        YOUR_DOMAIN = "http://127.0.0.1:8000/"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items=[
                {
                    'price_data':{
                        'currency':'usd',
                        'unit_amount':2000,
                        'product_data':{
                            'name':'Stubborn Attachments',
                        },
                    },
                    'quantity':1
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id':checkout_session.id
        })



class ProductLandingView(TemplateView):
    template_name = "cart/landing.html"




# @login_required(login_url="/login/")
# def place_order(request):
#     if request.method == "POST":
#         neworder  = Order()
#         neworder.user = request.user
#         neworder.firstname = request.POST.get('firstname')
#         neworder.lastname = request.POST.get('lastname')
#         neworder.email = request.POST.get('email')
#         neworder.phone = request.POST.get('phone')
#         neworder.address = request.POST.get('address')
#         neworder.city = request.POST.get('city')
#         neworder.state = request.POST.get('state')
#         neworder.country = request.POST.get('country')
#         neworder.postcode = request.POST.get('postcode')
#         neworder.payment_mode = request.POST.get('payment_mode')

#         cart = Cart.obj

#         return redirect('home')
#     return render(request, 'cart/placeorder.html')







# ---------------------------- Wishlist Function--------------------------

