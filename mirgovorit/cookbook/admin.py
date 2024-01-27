from django.contrib import admin

from .models import Product, Recipe, Weight


class ProductsInline(admin.StackedInline):
    model = Recipe.products.through
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    list_display_links = 'id', 'name'
    inlines = ProductsInline,

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('weight_set')
        return qs


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    list_display_links = 'id', 'name'
