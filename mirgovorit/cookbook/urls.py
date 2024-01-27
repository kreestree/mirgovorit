from django.urls import path

from . import views

urlpatterns = [
    path('add-product-to-recipe/', views.add_product_to_recipe, name='add-product-to-recipe'),
    path('cook-recipe/', views.cook_recipe, name='cook-recipe'),
    path('show-recipes-without-product/', views.show_recipes_without_product, name='show-recipes-without-product')
]
