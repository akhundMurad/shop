from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=512, verbose_name='название')
    cost_price = models.PositiveIntegerField(verbose_name='себестоимость')
    price = models.PositiveIntegerField(verbose_name='цена')
    quantity = models.IntegerField(verbose_name='количество')

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Order(models.Model):
    class Status(models.TextChoices):
        CANCELED = 'canceled', 'отменен'
        ON_PROCESSING = 'on_processing', 'на обработке'

    status = models.CharField(
        choices=Status.choices,
        max_length=13,
        verbose_name='статус'
    )
    products = models.ManyToManyField(
        'products.Product',
        verbose_name='продукты'
    )
    total_cost_price = models.PositiveIntegerField(
        verbose_name='итоговая себестоимость'
    )
    total_price = models.PositiveIntegerField(verbose_name='итоговая цена')
    created_at = models.DateTimeField(
        auto_created=True,
        verbose_name='дата создания'
    )
    products_quantity = models.PositiveIntegerField(
        verbose_name='количество продуктов'
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
