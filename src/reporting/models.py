from django.db import models


class Report(models.Model):
    class Meta:
        verbose_name = 'отчет'
        verbose_name_plural = 'отчеты'

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        verbose_name='продукт'
    )

    proceeds = models.PositiveIntegerField(
        default=0,
        verbose_name='выручка'
    )
    earnings = models.IntegerField(
        default=0,
        verbose_name='прибыль'
    )
    number_of_sold = models.PositiveIntegerField(
        default=0,
        verbose_name='количество проданных'
    )
    number_of_canceled = models.PositiveIntegerField(
        default=0,
        verbose_name='количество возвратов'
    )

    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
