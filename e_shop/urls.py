from django.urls import path
from .views import *

urlpatterns = [
    path('', Main, name='main_url'),

    path('profile', ProfileView, name='profile_view_url'),
    path('profile_edit', ProfileEdit, name='profile_edit_url'),
    path('profile_delete', ProfileDelete, name='profile_delete_url'),

    path('register', Register, name='register_url'),

    path('forecast', ForecastView, name='forecast_url'),
    
    path('shop', ShopAlmaty, name='shop_url'),
    path('search', Search, name='search_url'),

    path('goods/<int:category_pk>', GoodByCategory, name='good_by_category_url'),
    path('good/<int:good_pk>', GoodDetail, name='good_detail_url'),
    path('goods', Goods, name='goods_url'),

    path('new_product', NewProduct, name='new_product_url'),

    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('cart/cart-detail/', cart_detail, name='cart_detail'),

    path('boughproduct', BoughProduct, name='bough_url'),
    path('history', History, name='history_url'),

    path('geolocation', Geolocation, name='geolocation_url'),

    path('status/seller', StatusSeller, name='status_seller_url'),

    path('messages/new/<int:item_pk>', newConversation, name='new'),
    path('messages', chats, name='chats'),
    path('messages/<int:pk>', detail, name='detail'),
]