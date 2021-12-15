from django.contrib.auth import get_user_model
from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from users.serializers import CustomUserSerializer

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingList, Tag)

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    """ сериалайзер ингридиентов """
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class TagSerializer(serializers.ModelSerializer):
    """ сериалайзер тегов """
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class ShowRecipeIngredientSerializer(serializers.ModelSerializer):
    """ сериалайзер для отображения списка ингридиентов с количеством """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class ShowRecipeSerializer(serializers.ModelSerializer):
    """ сериалайзер для сокращенного просмотра рецепта """
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class ShowRecipeFullSerializer(serializers.ModelSerializer):
    """ сериалайзер для полного просмотра рецепта +методы """
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return ShowRecipeIngredientSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj, user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingList.objects.filter(
            recipe=obj,
            user=request.user
        ).exists()


class AddRecipeIngredientSerializer(serializers.ModelSerializer):
    """ сериалайзер для добавления ингридиента и количества в рецепт """
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class AddRecipeSerializer(serializers.ModelSerializer):
    """ сериалайзер для добавления рецепта +валидаторы """
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    ingredients = AddRecipeIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate_ingredients(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise ValidationError('Добавьте ингридиент')
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise ValidationError('Не может быть отрицательным')
        ingredients_count = len(ingredients)
        ingredients_set = len(set([i['id'] for i in ingredients]))
        if ingredients_count > ingredients_set:
            raise ValidationError('Ингридиенты повторяются')
        return data

    def validate_tags(self, data):
        tags = self.initial_data.get('tags')
        if len(tags) == 0:
            raise serializers.ValidationError('Добавьте тег')
        unique_tags = set()
        for item in tags:
            if item in unique_tags:
                raise serializers.ValidationError('Теги повторяются')
            unique_tags.add(item)
        return data

    def validate_cooking_time(self, data):
        if data <= 0:
            raise ValidationError('Не может быть меньше 1')
        return data

    def add_recipe_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            if (RecipeIngredient.objects.
                    filter(recipe=recipe, ingredient=ingredient_id).exists()):
                amount += F('amount')
            RecipeIngredient.objects.update_or_create(
                recipe=recipe, ingredient=ingredient_id,
                defaults={'amount': amount})

    def create(self, validated_data):
        author = self.context.get('request').user
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.add_recipe_ingredients(ingredients_data, recipe)
        recipe.tags.set(tags_data)
        return recipe

    def update(self, recipe, validated_data):
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.cooking_time = validated_data.get('cooking_time',
                                                 recipe.cooking_time)
        recipe.image = validated_data.get('image', recipe.image)
        if 'ingredients' in self.initial_data:
            ingredients = validated_data.pop('ingredients')
            recipe.ingredients.clear()
            self.add_recipe_ingredients(ingredients, recipe)
        if 'tags' in self.initial_data:
            tags_data = validated_data.pop('tags')
            recipe.tags.set(tags_data)
        recipe.save()
        return recipe

    def to_representation(self, recipe):
        data = ShowRecipeSerializer(
            recipe, context={'request': self.context.get('request')}).data
        return data


class FavouriteSerializer(serializers.ModelSerializer):
    """ сериалайзер избранного +валидатор """
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Favorite
        fields = (
            'user',
            'recipe',
        )

    def validate(self, data):
        user = data['user']
        recipe_id = data['recipe'].id
        if Favorite.objects.filter(user=user, recipe__id=recipe_id).exists():
            raise ValidationError('Уже в избранном')
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShowRecipeSerializer(instance.recipe, context=context).data


class ShoppingListSerializer(serializers.ModelSerializer):
    """ сериалайзер списка покупок +валидатор """
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ShoppingList
        fields = (
            'user',
            'recipe',
        )

    def validate(self, data):
        user = data['user']
        recipe_id = data['recipe'].id
        if ShoppingList.objects.filter(user=user,
                                       recipe__id=recipe_id).exists():
            raise ValidationError('уже в списке')
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShowRecipeSerializer(instance.recipe, context=context).data
