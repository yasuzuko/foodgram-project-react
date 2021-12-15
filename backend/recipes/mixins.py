from rest_framework import mixins, viewsets


class RetriveAndListViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    pass