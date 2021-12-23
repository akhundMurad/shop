from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=512, verbose_name='название')
    cost_price = models.PositiveIntegerField(verbose_name='себестоимость')
    price = models.PositiveIntegerField(verbose_name='цена')
    quantity = models.IntegerField(verbose_name='количество')

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
