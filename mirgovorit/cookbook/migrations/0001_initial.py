# Generated by Django 5.0.1 on 2024-01-27 12:35

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('times_cooked', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Сколько раз приготовлено')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
            },
        ),
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Вес')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cookbook.product', verbose_name='Продукт')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cookbook.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Вес продуктов в рецептах',
                'verbose_name_plural': 'Вес продуктов в рецептах',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='products',
            field=models.ManyToManyField(related_name='recipes', through='cookbook.Weight', to='cookbook.product', verbose_name='Используемые продукты'),
        ),
    ]
