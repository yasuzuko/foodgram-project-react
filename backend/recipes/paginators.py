from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPaginator(PageNumberPagination):
    """ переопределяет параметр чтобы работал стандартный паджинатор DRF """
    page_size_query_param = 'limit'
