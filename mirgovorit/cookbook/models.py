from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class Product(models.Model):
    """Модель для продуктов"""
    name = models.CharField(max_length=200, verbose_name='Название')  # Название продукта
    times_cooked = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Сколько раз приготовлено'
    )  # Сколько раз было приготовлено с этим продуктом

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Recipe(models.Model):
    """Модель для рецептов"""
    name = models.CharField(max_length=200, verbose_name='Название')  # Название рецепта
    products = models.ManyToManyField('Product',
                                      related_name='recipes',
                                      through='Weight',
                                      verbose_name='Используемые продукты')  # Используемые продукты

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Weight(models.Model):
    """Модель для веса продукта, используемого в рецепте"""
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')  # Продукт
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name='Рецепт')  # Рецепт
    weight = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Вес',
    )  # Вес в граммах

    def __str__(self):
        return f'Продукт "{self.product.name}"'

    class Meta:
        verbose_name = 'Вес продуктов в рецептах'
        verbose_name_plural = 'Вес продуктов в рецептах'
