from django.urls import path, include

from products.views import product


app_name = 'products'

product_patters = [
    path(
        '',
        product.ProductListAPIView.as_view(),
        name='product-list'
    ),
    path(
        'create/',
        product.ProductCreateAPIView.as_view(),
        name='product-create'
    ),
    path(
        'partial-update/<int:pk>/',
        product.ProductPartialUpdateAPIView.as_view(),
        name='product-partial-update'
    )
]

urlpatterns = [
    path('product/', include(product_patters))
]
