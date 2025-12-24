from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'myapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:blog_id>/', views.single_blog, name='single_blog'),
    path('contact/', views.contact, name='contact'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout_view/', views.checkout_view, name='checkout_view'),

    # Cart URLs
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-quantity/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),

    # Shop URLs
    path('shop/', views.shop, name='shop'),
    path('shop/genre/<int:genre_id>/', views.shop_by_genre, name='shop_by_genre'),
    path('product/<int:genreId>/<int:productId>/', views.product_detail, name='single_product_details'),

    # Billing URLs
    path('billing/add/', views.billing_add, name='billing_add'),
    path('billing/list/', views.billing_list, name='billing_list'),
]