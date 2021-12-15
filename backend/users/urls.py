from django.urls import include, path
from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken import views
from djoser.views import TokenCreateView, TokenDestroyView


from .views import FollowApiView, ListFollowViewSet


# router = DefaultRouter()
#
# router.register('users', UserViewSet)

urlpatterns = [
    # подписки
    path('users/<int:id>/subscribe/', FollowApiView.as_view(),
         name='subscribe'),
    path('users/subscriptions/', ListFollowViewSet.as_view(),
         name='subscription'),
    # токен
    path('auth/token/login/', TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', TokenDestroyView.as_view(),
         name='logout'),
    # общие
    path('', include('djoser.urls')),

    ]
