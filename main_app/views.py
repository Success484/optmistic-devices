from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Wishlist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from decimal import Decimal
from django.db.models import Q


# Create your views here.

def HomePageView(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True).order_by('?')[:4]
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category).order_by('?')[:4]

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'banner_image1': 'images/banner1.jpg',
        'banner_image2': 'images/banner2.jpg',
    }
    return render(request, 'main/index.html', context)


def AboutPageView(request):
    context = {
        'banner_AboutUs': 'images/hero-image.jpg',
    }
    return render(request, 'main/about.html', context)


def blogPageView(request):
    context = {
        'banner_blog': 'images/hero-image1.jpg',
    }
    return render(request, 'main/blog.html', context)


def contactPageView(request):
    context = {
        'banner_image2': 'images/banner2.jpg',
    }
    return render(request, 'main/contact.html', context)


def ShopPageView(request, category_slug=None, product_id=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)

    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    product_detail = None
    if product_id:
        product_detail = get_object_or_404(Product, pk=product_id)
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'product_detail': product_detail,
        'query': query,
        'banner_contact': 'images/hero-image.jpg',
    }
    return render(request, 'main/shop.html', context)

def get_product(product_id):
    return get_object_or_404(Product, pk=product_id)


def CartPageView(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            quantity = item.get('quantity', 1)
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            continue
    extra_charge = total * Decimal(0.05)
    grand_total = total + extra_charge

    context = {
        'cart_items': cart_items,
        'total': grand_total,
    }
    return render(request, 'main/cart.html', context)

@csrf_exempt  # use CSRF token in JS (preferred for production)
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        # Get product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
        
        # Initialize cart in session if it doesn't exist
        cart = request.session.get('cart', {})
        
        # Add or update item
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += quantity
        else:
            cart[str(product_id)] = {
                'name': product.name,
                'price': float(product.price),
                'quantity': quantity,
                'image': product.image.url if product.image else '/static/images/default-product.jpg'
            }
        
        # Save to session
        request.session['cart'] = cart
        request.session.modified = True
        
        return JsonResponse({'success': True, 'cart_count': sum(item['quantity'] for item in cart.values())})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


@csrf_exempt
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')  # 'increase' or 'decrease'

        cart = request.session.get('cart', {})

        if product_id in cart:
            if action == 'increase':
                cart[product_id]['quantity'] += 1
            elif action == 'decrease':
                cart[product_id]['quantity'] -= 1
                if cart[product_id]['quantity'] <= 0:
                    del cart[product_id]

        request.session['cart'] = cart
        request.session.modified = True

        # Calculate totals
        total = sum(item['price']*item['quantity'] for item in cart.values())

        return JsonResponse({
            'success': True,
            'cart': cart,
            'total': total
        })

    return JsonResponse({'success': False}, status=400)


@csrf_exempt
def remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart', {})

        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
            request.session.modified = True

        # Calculate totals
        total = sum(item['price']*item['quantity'] for item in cart.values())

        return JsonResponse({'success': True, 'cart': cart, 'total': total})

    return JsonResponse({'success': False}, status=400)


@csrf_exempt
def add_to_wishlist(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        # Try to get the product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)

        # Initialize wishlist in session if not exists
        wishlist = request.session.get('wishlist', {})

        # Add product if not already in wishlist
        if str(product_id) not in wishlist:
            wishlist[str(product_id)] = {
                'name': product.name,
                'price': float(product.price),
                'image': product.image.url if product.image else '/static/images/default-product.jpg'
            }
            message = 'Product added to wishlist'
        else:
            message = 'Product already in wishlist'

        # Save to session
        request.session['wishlist'] = wishlist
        request.session.modified = True

        return JsonResponse({
            'success': True,
            'wishlist_count': len(wishlist),
            'message': message
        })

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def wishlistPageView(request):
    wishlist = request.session.get('wishlist', {})
    return render(request, 'shop/wishlist.html', {'wishlist': wishlist})


@csrf_exempt
def remove_from_wishlist(request):
    # Remove an item from the user's wishlist (stored in session).
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        wishlist = request.session.get('wishlist', {})

        if product_id in wishlist:
            del wishlist[product_id]
            request.session['wishlist'] = wishlist
            request.session.modified = True

            # Return updated wishlist count and success
            return JsonResponse({
                'success': True,
                'wishlist': wishlist,
                'wishlist_count': len(wishlist)
            })

        # Item not found in wishlist
        return JsonResponse({'success': False, 'message': 'Item not found in wishlist'}, status=404)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def productDetailPageView(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    related_products = Product.objects.filter(category=product.category,is_available=True).exclude(id=product.id).order_by('?')[:3]
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'main/detail.html', context)
 

def checkOutPageView(request):
    return render(request, 'main/checkout.html')
