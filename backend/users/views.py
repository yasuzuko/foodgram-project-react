from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Follow
from recipes.paginators import CustomPageNumberPaginator
from .serializers import FollowSerializer, ShowFollowSerializer

User = get_user_model()


class FollowApiView(APIView):
    """ класс для работы с подписками """
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, id):
        data = {'user': request.user.id, 'following': id}
        serializer = FollowSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        subscription = get_object_or_404(Follow, user=user,
                                         following=following)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListFollowViewSet(generics.ListAPIView):
    """ класс для списка подписок """
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ShowFollowSerializer
    pagination_class = CustomPageNumberPaginator

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)
