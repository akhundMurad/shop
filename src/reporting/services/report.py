from django.db.models import Sum, Q
from django.utils import timezone

from products.models import Product, Order
from reporting.models import Report


TODAY = timezone.now().today()


def create_reports():
    reports: list[Report] = list()

    for product in Product.objects.prefetch_related(
            'orderedproduct_set'
    ).iterator():
        report = create_report_for_product(product)
        reports.append(report)

    Report.objects.bulk_create(reports)


def create_report_for_product(product: Product) -> Report:
    ordered_products = product.orderedproduct_set.select_related(
        'order', 'product'
    ).filter(order__created_at__date=TODAY)
    sold_ordered_products = ordered_products.filter(
        order__status=Order.Status.DONE
    )

    data = sold_ordered_products.aggregate(
        product_quantity_sum=Sum('product_quantity')
    )

    cost_price = data.get('product_quantity_sum', 0) * product.cost_price
    proceeds = data.get('product_quantity_sum', 0) * product.price

    number_of_sold = sold_ordered_products.count()
    number_of_canceled = ordered_products.filter(
        order__status=Order.Status.CANCELED
    ).count()

    return Report(
        product=product,
        proceeds=proceeds,
        earnings=proceeds - cost_price,
        number_of_sold=number_of_sold,
        number_of_canceled=number_of_canceled
    )
