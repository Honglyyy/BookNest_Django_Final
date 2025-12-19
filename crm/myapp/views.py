from django.db.models import Sum, Avg, aggregates
from django.http import HttpResponse
from django.shortcuts import render, redirect
from myapp.models import Genre, Category, Product, BillingDetail


def index(request):
    DTProduct = Product.objects.all()
    context = {
        'DTProduct': DTProduct,
    }
    return render(request, 'myapp/index.html', context)


def blog(request):
    return render(request, 'myapp/blog.html')


def contact(request):
    return render(request, 'myapp/contact.html')


def checkout(request):
    return render(request, 'myapp/checkout.html')


def add_to_cart(request, product_id):
    """Add product to cart or increase quantity if already exists"""
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
        cart[str(product_id)]['total'] = cart[str(product_id)]['quantity'] * cart[str(product_id)]['price']
    else:
        try:
            product = Product.objects.get(id=product_id)
            cart[str(product_id)] = {
                'productName': product.productName,
                'price': float(product.price),
                'quantity': 1,
                'total': float(product.price) * 1,
                'image': product.productImage.url if product.productImage else ''
            }
        except Product.DoesNotExist:
            return redirect('shop')

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('view_cart')


def view_cart(request):
    """Display cart contents"""
    cart = request.session.get('cart', {})
    total_price = sum(item['total'] for item in cart.values())

    context = {
        'cart': cart,
        'total_price': total_price
    }
    return render(request, 'myapp/cart.html', context)


def remove_from_cart(request, product_id):
    """Remove item completely from cart"""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart.pop(str(product_id), None)
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('view_cart')


def update_cart_quantity(request, product_id):
    """Update quantity of item in cart (increase or decrease)"""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        action = request.POST.get('action')

        if str(product_id) in cart:
            if action == 'increase':
                cart[str(product_id)]['quantity'] += 1
            elif action == 'decrease' and cart[str(product_id)]['quantity'] > 1:
                cart[str(product_id)]['quantity'] -= 1

            # Recalculate total for this item
            cart[str(product_id)]['total'] = (
                    cart[str(product_id)]['quantity'] * cart[str(product_id)]['price']
            )

            request.session['cart'] = cart
            request.session.modified = True

    return redirect('view_cart')


def shop(request):
    DTProduct = Product.objects.all()
    DTCategory = Category.objects.prefetch_related('genres')
    NumOfProducts = Product.objects.count()

    context = {
        'DTProduct': DTProduct,
        'DTCategory': DTCategory,
        'NumOfProducts': NumOfProducts,
    }
    return render(request, 'myapp/shop.html', context)


def shop_by_genre(request, genre_id):
    DTProduct = Product.objects.filter(genreID_id=genre_id)
    DTCategory = Category.objects.prefetch_related('genres')
    NumOfProducts = DTProduct.count()

    context = {
        'DTProduct': DTProduct,
        'DTCategory': DTCategory,
        'NumOfProducts': NumOfProducts,
    }
    return render(request, 'myapp/shop.html', context)


def single_blog(request):
    return render(request, 'myapp/single-blog.html')


def product_detail(request, genreId, productId):
    DTProduct = Product.objects.get(genreID_id=genreId, id=productId)
    DTAllProduct = Product.objects.all()
    context = {
        'DTProduct': DTProduct,
        'DTAllProduct': DTAllProduct,
    }
    return render(request, 'myapp/single-product-details.html', context)

def checkout_view(request):
    cart = request.session.get('cart', {})
    total_price = sum(item['total'] for item in cart.values())

    return render(request, 'myapp/checkout.html', {
        'cart': cart,
        'total_price': total_price,
    })

def billing_add(request):
    cart = request.session.get('cart', {})
    total_price = sum(item['total'] for item in cart.values())

    if request.method == "POST":
        data = request.POST
        qr_image = request.FILES.get('qr_code_image')

        billing = BillingDetail(
            first_name=data['first_name'],
            last_name=data['last_name'],
            country=data['country'],
            address1=data['address1'],
            address2=data['address2'],
            postcode=data['postcode'],
            town=data['town'],
            phone=data['phone'],
            email=data['email'],
            qr_code_image=qr_image,
            total=data['total']
        )
        billing.save()
        return redirect('billing_list')

    return render(request, 'myapp/checkout.html', {
        'cart': cart,
        'total_price': total_price,
    })
def billing_list(request):
    billings = BillingDetail.objects.all()
    return render(request, 'myapp/billing_list.html', {'billings': billings})