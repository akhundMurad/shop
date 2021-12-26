from django.core.exceptions import ValidationError
from django.db import models


class Product(models.Model):
    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    name = models.CharField(max_length=512, verbose_name='название')
    cost_price = models.PositiveIntegerField(
        verbose_name='себестоимость',
        default=0
    )
    price = models.PositiveIntegerField(
        verbose_name='цена',
        default=0
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0
    )

    def clean(self):
        if self.cost_price > self.price:
            raise ValidationError(
                'The cost price cannot be higher than price.'
            )


class Order(models.Model):
    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    class Status(models.TextChoices):
        CANCELED = 'canceled', 'отменен'
        ON_PROCESSING = 'on_processing', 'на обработке'
        DONE = 'done', 'завершен'

    status = models.CharField(
        choices=Status.choices,
        max_length=13,
        verbose_name='статус'
    )
    products = models.ManyToManyField(
        'products.Product',
        through='products.OrderedProduct',
        verbose_name='продукты'
    )
    total_cost_price = models.PositiveIntegerField(
        verbose_name='итоговая себестоимость',
        default=0
    )
    total_price = models.PositiveIntegerField(
        verbose_name='итоговая цена',
        default=0
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    products_quantity = models.PositiveIntegerField(
        verbose_name='количество продуктов',
        default=0
    )


class OrderedProduct(models.Model):
    class Meta:
        verbose_name = 'заказанный продукт'
        verbose_name_plural = 'заказанные продукты'

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        verbose_name='продукт'
    )
    order = models.ForeignKey(
        'products.Order',
        on_delete=models.CASCADE
    )
    product_quantity = models.PositiveIntegerField(
        verbose_name='количество продуктов',
        default=0
    )
