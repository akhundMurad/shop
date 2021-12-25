import factory.fuzzy
from factory.django import DjangoModelFactory

from .models import Product, Order


class ProductFactory(DjangoModelFactory):
    name = factory.Faker('word')
    cost_price = factory.fuzzy.FuzzyInteger(5, 12)
    price = factory.fuzzy.FuzzyInteger(14, 20)
    quantity = factory.fuzzy.FuzzyInteger(100, 200)

    class Meta:
        model = Product


class OrderFactory(DjangoModelFactory):
    status = factory.Iterator([choice[0] for choice in Order.Status.choices])
    total_cost_price = factory.fuzzy.FuzzyInteger(5, 12)
    total_price = factory.fuzzy.FuzzyInteger(14, 20)
    products_quantity = factory.fuzzy.FuzzyInteger(1, 10)

    class Meta:
        model = Order
