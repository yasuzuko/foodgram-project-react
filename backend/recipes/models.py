from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Тег',
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет',
    )
    slug = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения',
        default=1,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        default=timezone.now,
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    text = models.TextField(
        verbose_name='Текст рецепта',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='tags',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления'
    )
    image = models.ImageField(
        upload_to='recipes/images',
        verbose_name='Картинка'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        verbose_name='Ингредиент',
        related_name='ingredients',
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'], name='unique_ingredient')]

    def __str__(self):
        return 'Ингредиенты'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorite',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Избранное'
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_recipe_in_user_favorite')]


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_recipe_in_user_shopping_list')]
        ordering = ('-id',)
        verbose_name = 'Список покупок'
