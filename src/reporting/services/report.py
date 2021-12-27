from datetime import date

from django.db.models import Sum, Q, QuerySet, Count
from django.utils import timezone

from products.models import Product, Order
from reporting.models import Report


def create_reports():
    today = timezone.now().today()
    reports: list[Report] = list()

    for product in Product.objects.prefetch_related(
            'orderedproduct_set'
    ).iterator():
        report = create_report_for_product(product, today)
        reports.append(report)

    Report.objects.bulk_create(reports)


def create_report_for_product(product: Product, today: date) -> Report:
    ordered_products = product.orderedproduct_set.select_related(
        'order', 'product'
    ).filter(order__created_at__date=today)

    sold_data = _get_sold_ordered_products_data(ordered_products)
    sold_sum = sold_data.get(
        'product_quantity_sum', 0
    )

    canceled_data = _get_canceled_ordered_products_data(ordered_products)
    canceled_sum = canceled_data.get(
        'product_quantity_sum', 0
    )

    cost_price = sold_sum * product.cost_price
    proceeds = sold_sum * product.price

    number_of_sold = sold_data['count'] * sold_sum
    number_of_canceled = canceled_data['count'] * canceled_sum

    return Report(
        product=product,
        proceeds=proceeds,
        earnings=proceeds - cost_price,
        number_of_sold=number_of_sold,
        number_of_canceled=number_of_canceled
    )


def _get_sold_ordered_products_data(ordered_products: QuerySet) -> dict:
    sold_ordered_products = ordered_products.filter(
        order__status=Order.Status.DONE
    )

    data = sold_ordered_products.aggregate(
        product_quantity_sum=Sum('product_quantity'),
        count=Count('id', distinct=True)
    )

    return data


def _get_canceled_ordered_products_data(ordered_products: QuerySet) -> dict:
    canceled_ordered_products = ordered_products.filter(
        order__status=Order.Status.CANCELED
    )

    data = canceled_ordered_products.aggregate(
        product_quantity_sum=Sum('product_quantity'),
        count=Count('id', distinct=True)
    )

    return data
