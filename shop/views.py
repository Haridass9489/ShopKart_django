from django.shortcuts import render ,redirect
from django.http import HttpResponse,JsonResponse
from . models import *
from django.contrib import messages
from shop.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
import json

# Create your views here.

def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,'shop/index.html',{'products':products})

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Successfully Logged out...")
        return redirect('/')

def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,'shop/cart.html',{'cart':cart})
    else:
        return redirect('/login')

def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      product_id=data['pid']
      #print(request.user.id)
      product_status=Product.objects.get(id=product_id)
      if product_status:
        if Cart.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Cart'}, status=200)
        else:
          if product_status.quantity>=product_qty:
            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
            return JsonResponse({'status':'Product Added to Cart'}, status=200)
          else:
            return JsonResponse({'status':'Product Stock Not Available'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)

def removecart(request,cid):
   cartItem = Cart.objects.get(id=cid)
   cartItem.delete()
   return redirect('/cart')

def fav(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
        if Fav.objects.filter(user=request.user.id,product_id=product_id):
            return JsonResponse({'status':'Product Already in Favourite'}, status=200)
        else:
            Fav.objects.create(user=request.user,product_id=product_id)
            return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)

def removefav(request,fid):
   favItem = Fav.objects.get(id=fid)
   favItem.delete()
   return redirect('/favpage')

def favpage(request):
    if request.user.is_authenticated:
        fav=Fav.objects.filter(user=request.user)
        return render(request,'shop/fav.html',{'fav':fav})
    else:
        return redirect('/login')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Successfully Logged in...")
                return redirect('/')
            else:
                messages.success(request,"Invalid User...")
                return redirect('/login')
        return render(request,'shop/login.html')

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Resistration Successful...")
            return redirect('/login')
    return render(request,'shop/register.html',{'form':form})

def collections(request):
    catagory = Catagory.objects.filter(status=0)
    return render(request,'shop/collections.html',{'catagory':catagory})

def collectionsviews(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products = Product.objects.filter(Catagory__name=name)
        return render(request,'shop/products/index.html',{'products':products,'category_name':name})
    else:
        messages.warning("No such category has found")
        return redirect('collections')

def product_details(request,pname,cname):
    if (Catagory.objects.filter(name=cname,status=0)):
        if (Product.objects.filter(name=pname,status=0)):
            products = Product.objects.filter(name=pname,status=0).first()    
            return render(request,"shop/products/productdetails.html",{'products':products})
        else:
            messages.warning("No such product has found")
            return redirect('collections')
    else:
        messages.warning("No such category has found")
        return redirect('collections')


