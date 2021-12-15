from django_filters import rest_framework as filters

from .models import Ingredient, Recipe


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        label='Tags',
    )
    is_favorited = filters.BooleanFilter(
        method='get_favorite',
        label='Favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_shopping',
        label='Is in shopping list',
    )

    class Meta:
        model = Recipe
        fields = (
            'is_favorited',
            'author',
            'tags',
            'is_in_shopping_cart'
        )

    def get_favorite(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(in_favorite__user=self.request.user)
        return Recipe.objects.all()

    def get_shopping(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(shoppinglist__user=self.request.user)
        return Recipe.objects.all()
