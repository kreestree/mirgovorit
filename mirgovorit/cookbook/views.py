from django.core.exceptions import ValidationError
from django.db.models import F, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Recipe, Product, Weight


# Create your views here.
def add_product_to_recipe(request: HttpRequest) -> HttpResponse:
    """
    Функция добавляет к указанному рецепту указанный продукт с указанным весом.
    Если в рецепте уже есть такой продукт, то функция должна поменять его вес в этом рецепте на указанный.
    :param request:
    :return:
    """
    recipe_id = request.GET.get('recipe_id')
    product_id = request.GET.get('product_id')
    weight = request.GET.get('weight')

    if recipe_id and product_id and weight:  # Проверка, что в GET-запросе есть все параметры
        if int(weight) < 0:
            raise ValidationError('Вес не может быть меньше 0')

        recipe = get_object_or_404(Recipe, id=recipe_id)  # Получение рецепта по указанному ID
        product = get_object_or_404(Product, id=product_id)  # Получение продукта по указанному ID
        if recipe.products.filter(id=product_id).exists():  # Проверка, есть ли продукт в рецепте
            recipe.weight_set.filter(product=product).update(weight=weight)
        else:
            Weight.objects.create(product=product, recipe=recipe, weight=weight)

    context = {'recipe_id': recipe_id,
               'product_id': product_id,
               'weight': weight}
    return render(request, 'cookbook/add-products.html', context=context)


def cook_recipe(request: HttpRequest) -> HttpResponse:
    """
    Функция увеличивает на единицу количество приготовленных блюд для каждого продукта, входящего в указанный рецепт
    :param request:
    :return:
    """
    recipe_id = request.GET.get('recipe_id')  # Получение рецепта по указанному ID
    if recipe_id:  # Проверка, что в GET-запросе есть параметр
        recipe = get_object_or_404(Recipe, id=recipe_id)  # Получение рецепта по указанному ID
        products = recipe.products.all()  # Получение продуктов, входящих в рецепт
        products.update(times_cooked=F('times_cooked') + 1)  # +1 к количеству приготовлений в продуктах
    context = {'recipe_id': recipe_id}
    return render(request, 'cookbook/cook-recipe.html', context=context)


def show_recipes_without_product(request: HttpRequest) -> HttpResponse:
    """
     Функция возвращает HTML страницу, на которой размещена таблица.
     В таблице отображены id и названия всех рецептов, в которых указанный продукт отсутствует,
     или присутствует в количестве меньше 10 грамм.
    :param request:
    :return:
    """
    product_id = request.GET.get('product_id')  # Получение продукта по указанному ID
    context = {
        'product_id': product_id,
    }

    if product_id:  # Проверка, что в GET-запросе есть параметр
        product = get_object_or_404(Product, id=product_id)  # Получение продукта по указанному ID
        recipes_contains_product = product.weight_set.filter(weight__gte=10)  # Получение рецептов, содержащих продукт
        id_list_contains_product = list(
            weight.recipe.id
            for weight in recipes_contains_product
        )  # Получение списка ID рецептов, содержащих продукт
        recipes_not_contains_product = Recipe.objects.filter(
            ~Q(id__in=id_list_contains_product)
        )  # Получение рецептов, чей ID не входит в вышестоящей таблице
        context['recipes'] = recipes_not_contains_product

    return render(request, 'cookbook/show-recipes-without-product.html', context=context)
