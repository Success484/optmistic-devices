from django.urls import path
from main_app.views import (HomePageView, AboutPageView, blogPageView, contactPageView, 
                            ShopPageView, CartPageView, productDetailPageView, checkOutPageView, 
                            wishlistPageView, add_to_cart, remove_from_cart, update_cart, 
                            add_to_wishlist, remove_from_wishlist)

urlpatterns = [
    path('', HomePageView, name="HomePageView"),
    path('about/', AboutPageView, name="AboutPageView"),
    path('blog/', blogPageView, name='blogPageView'),
    path('contact/', contactPageView, name='contactPageView'),
    path('shop/', ShopPageView, name='ShopPageView'),
    path('shop/product/<int:product_id>/', ShopPageView, name='shop-product-only'),
    path('detail/<int:product_id>/', productDetailPageView, name='detailPageView'),
    path('cart/', CartPageView, name='CartPageView'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('update-cart/', update_cart, name='update_cart'),
    path('remove-from-cart/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkOutPageView, name='checkOutPageView'),
    path('wishlist/', wishlistPageView, name='wishlistPageView'),
    path('add-to-wishlist/', add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/', remove_from_wishlist, name='remove_from_wishlist'),
]