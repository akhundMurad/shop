from django.urls import path, include

from products.views import product


app_name = 'products'

product_patters = [
    path(
        '',
        product.ProductListAPIView.as_view(),
        name='product-list'
    ),
]

urlpatterns = [
    path('product/', include(product_patters))
]
