from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),
    path('addtocart',views.add_to_cart,name='addtocart'),
    path('removecart/<str:cid>',views.removecart,name='removecart'),
    path('cart',views.cart_page,name='cart'),
    path('fav',views.fav,name='fav'),
    path('removefav/<str:fid>',views.removefav,name='removefav'),
    path('favpage',views.favpage,name='favpage'),
    path('collections',views.collections,name='collections'),
    path('collections/<str:name>',views.collectionsviews,name='collections'),
    path('collections/<str:cname>/<str:pname>',views.product_details,name='productdetails'),
]