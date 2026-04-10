def cart_and_wishlist_counts(request):
    cart = request.session.get('cart', {})
    wishlist = request.session.get('wishlist', {})

    return {
        'cart_count': len(cart),
        'wishlist_count': len(wishlist),
    }
