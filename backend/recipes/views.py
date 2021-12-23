from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .mixins import RetriveAndListViewSet
from .models import (Favorite, Ingredient, Recipe,
                     ShoppingList, Tag)
from .paginators import CustomPageNumberPaginator
from .permissions import IsAuthorOrAdmin
from .serializers import (AddRecipeSerializer, FavouriteSerializer,
                          IngredientSerializer, ShoppingListSerializer,
                          ShowRecipeFullSerializer, TagSerializer)


class IngredientViewSet(RetriveAndListViewSet):
    """ вьюсет для ингридиентов рецептов """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    pagination_class = None
    filterset_class = IngredientFilter


class TagsViewSet(RetriveAndListViewSet):
    """ вьюсет для тегов """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """ вьюсет для рецептов + методы для избранного и списка покупок """
    queryset = Recipe.objects.all().order_by('-id')
    serializer_class = ShowRecipeFullSerializer
    permission_classes = [IsAuthorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPageNumberPaginator
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowRecipeFullSerializer
        return AddRecipeSerializer

    @action(detail=True, permission_classes=[IsAuthorOrAdmin])
    def favorite(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = FavouriteSerializer(data=data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, permission_classes=[IsAuthorOrAdmin])
    def shopping_cart(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = ShoppingListSerializer(data=data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_list = get_object_or_404(ShoppingList,
                                          user=user, recipe=recipe)
        shopping_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        print('download_shopping_cart')
        name = 'recipe__ingredients__name'
        unit = 'recipe__ingredients__measurement_unit'
        amount = 'recipe__ingredients__ingredients__amount'
        user = request.user
        shopping_list = ShoppingList.objects.filter(
            user=user
            ).order_by(name).values(name, unit).annotate(amount=Sum(amount))
        text = 'Список покупок:\n\n'
        for number, item in enumerate(shopping_list, start=1):
            text += f'{number}) {item[name]} - {item["amount"]} {item[unit]}\n'
        response = HttpResponse(text, 'Content-Type: text/plain')
        filename = 'purchase.txt'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
