import factory.fuzzy
from factory.django import DjangoModelFactory

from reporting.models import Report


class ReportFactory(DjangoModelFactory):
    class Meta:
        model = Report

    product = factory.SubFactory(
        'products.factories.ProductFactory'
    )
    proceeds = factory.fuzzy.FuzzyInteger(50, 100)
    earnings = factory.fuzzy.FuzzyInteger(10, 40)
    number_of_sold = factory.fuzzy.FuzzyInteger(5, 15)
    number_of_canceled = factory.fuzzy.FuzzyInteger(1, 5)
