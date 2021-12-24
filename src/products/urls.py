from django.urls import path, include

from products.views import product, order, orderedproduct

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

order_patterns = [
    path(
        'partial-update/<int:pk>/',
        order.OrderPartialUpdateAPIView.as_view(),
        name='order-partial-update'
    )
]


ordered_product_patterns = [
    path(
        'bulk-create/',
        orderedproduct.OrderedProductBulkCreateAPIView.as_view(),
        name='ordered-product-bulk-create'
    )
]


urlpatterns = [
    path('product/', include(product_patters)),
    path('order/', include(order_patterns)),
    path('ordered-product/', include(ordered_product_patterns))
]
