import factory.fuzzy
from factory.django import DjangoModelFactory

from .models import Product


class ProductFactory(DjangoModelFactory):
    name = factory.Faker('word')
    cost_price = factory.fuzzy.FuzzyInteger(5, 12)
    price = factory.fuzzy.FuzzyInteger(14, 20)
    quantity = factory.fuzzy.FuzzyInteger(100, 200)

    class Meta:
        model = Product
