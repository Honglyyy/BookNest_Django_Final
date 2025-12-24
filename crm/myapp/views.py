from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, Avg, aggregates
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from myapp.models import Genre, Category, Product, BillingDetail, Blog


def index(request):
    DTProduct = Product.objects.all()
    context = {
        'DTProduct': DTProduct,
    }
    return render(request, 'myapp/index.html', context)


def blog(request):
    # Get all blogs ordered by newest first
    DTBlog = Blog.objects.all().order_by('-addedDate')

    # Paginate - 3 blogs per page
    paginator = Paginator(DTBlog, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'DTBlog': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'myapp/blog.html', context)


def single_blog(request, blog_id):
    blog = get_object_or_404(Blog, blogID=blog_id)

    related_blogs = Blog.objects.exclude(blogID=blog_id).order_by('-addedDate')[:4]

    context = {
        'blog': blog,
        'related_blogs': related_blogs,
    }
    return render(request, 'myapp/single-blog.html', context)


def contact(request):
    return render(request, 'myapp/contact.html')


def checkout(request):
    return render(request, 'myapp/checkout.html')


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)

        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += quantity
        else:
            cart[str(product_id)] = {
                'productName': product.productName,
                'price': float(product.price),
                'quantity': quantity,
                'image': product.productImage.url if product.productImage else ''
            }

        # Update total
        cart[str(product_id)]['total'] = (
            cart[str(product_id)]['price'] *
            cart[str(product_id)]['quantity']
        )

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('myapp:view_cart')


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
    return redirect('myapp:view_cart')


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

    return redirect('myapp:view_cart')


def shop(request):
    # Get all products
    DTProduct = Product.objects.all()

    # Apply sorting BEFORE pagination
    sort_by = request.GET.get('select', 'newest')

    if sort_by == 'newest':
        DTProduct = DTProduct.order_by('-addedDate')
    elif sort_by == 'price_high_low':
        DTProduct = DTProduct.order_by('-price')
    elif sort_by == 'price_low_high':
        DTProduct = DTProduct.order_by('price')

    # Now paginate the sorted queryset
    paginator = Paginator(DTProduct, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get categories
    DTCategory = Category.objects.prefetch_related('genres')

    context = {
        'DTProduct': page_obj,  # Pass the paginated object, not the full queryset
        'DTCategory': DTCategory,
        'NumOfProducts': paginator.count,  # Use paginator.count for total
        'current_sort': sort_by,
        'page_obj': page_obj,
    }
    return render(request, 'myapp/shop.html', context)


def shop_by_genre(request, genre_id):
    # Get products filtered by genre
    DTProduct = Product.objects.filter(genreID_id=genre_id)

    # Apply sorting BEFORE pagination
    sort_by = request.GET.get('select', 'newest')

    if sort_by == 'newest':
        DTProduct = DTProduct.order_by('-addedDate')
    elif sort_by == 'price_high_low':
        DTProduct = DTProduct.order_by('-price')
    elif sort_by == 'price_low_high':
        DTProduct = DTProduct.order_by('price')

    # Paginate the sorted queryset
    paginator = Paginator(DTProduct, 9)  # 9 products per page (3x3 grid)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get other data
    DTCategory = Category.objects.prefetch_related('genres')
    current_genre = get_object_or_404(Genre, id=genre_id)

    context = {
        'DTProduct': page_obj,  # Pass paginated object
        'DTCategory': DTCategory,
        'NumOfProducts': paginator.count,  # Total count
        'current_sort': sort_by,
        'genre_id': genre_id,
        'current_genre': current_genre,
        'page_obj': page_obj,  # For pagination controls
    }
    return render(request, 'myapp/shop_by_genre.html', context)


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
        return redirect('myapp:billing_list')

    return render(request, 'myapp/checkout.html', {
        'cart': cart,
        'total_price': total_price,
    })


def billing_list(request):
    billings = BillingDetail.objects.all()
    return render(request, 'myapp/billing_list.html', {'billings': billings})