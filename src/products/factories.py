import factory.fuzzy
from factory.django import DjangoModelFactory

from .models import Product, Order, OrderedProduct


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')
    cost_price = factory.fuzzy.FuzzyInteger(5, 12)
    price = factory.fuzzy.FuzzyInteger(14, 20)
    quantity = factory.fuzzy.FuzzyInteger(100, 200)


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    status = factory.Iterator([choice[0] for choice in Order.Status.choices])
    total_cost_price = factory.fuzzy.FuzzyInteger(5, 12)
    total_price = factory.fuzzy.FuzzyInteger(14, 20)
    products_quantity = factory.fuzzy.FuzzyInteger(1, 10)


class OrderedProductFactory(DjangoModelFactory):
    class Meta:
        model = OrderedProduct

    product = factory.SubFactory(ProductFactory)
    order = factory.SubFactory(OrderFactory)
    product_quantity = factory.fuzzy.FuzzyInteger(1, 10)
