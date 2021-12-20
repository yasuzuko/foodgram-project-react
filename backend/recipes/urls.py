from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagsViewSet

router = DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
