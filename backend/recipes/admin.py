from django.contrib import admin

from .models import (
    Ingredient,
    Recipe,
    Tag,
    RecipeIngredient,
    RecipeTag,
    Favorite,
    ShoppingList,
)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    min_num = 1
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        RecipeIngredientInline,
        RecipeTagInline,
    )
    list_display = ('name', 'text', 'cooking_time')
    search_fields = ('name', 'text', 'ingredients')
    empty_value_display = '- пусто -'
    list_filter = ('author', 'name', 'tags')





@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
