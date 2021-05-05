from django.db import models


class Product(models.Model):
    name = models.CharField('Имя товара', max_length=100)
    photo = models.ImageField('Фото png', upload_to='shop/')
    quantity = models.PositiveIntegerField('Количество товара')
    price = models.DecimalField('Цена', max_digits=5, decimal_places=2)
    is_published = models.BooleanField('Показывать?', default=True)

    def __str__(self):
        return f'Товар {self.name} в количестве {self.quantity}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
