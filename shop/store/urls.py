from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category_page'),
    path('product_detail/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('search/', SearchResults.as_view(), name='search'),
    path('add_favorite/<slug:slug>/', save_favorite_products, name='add_favorite'),
    path('my_favorite/', FavoriteProductView.as_view(), name='my_favorite'),
    path('mail/', mail_view, name='mail'),
    path('save_email/', save_mail_customer, name='save_email'),
    path('send_mail/', send_mail_to_customer, name='send_mail'),
    path('cart/', cart, name='my_cart'),
    path('to_cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),
    path('checkout/', checkout, name='checkout'),
    path('payment/', create_checkout_session, name='payment'),
    path('success/', success_payment, name='success'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('about/', about, name='about'),
    path('profile/<int:pk>', profile_view, name='profile'),
    path('change_account/', edit_account_view, name='change_account'),
    path('change_profile/', edit_profile_view, name='change_profile')
]
