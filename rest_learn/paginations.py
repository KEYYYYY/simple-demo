from rest_framework import pagination


class GoodsPagination(pagination.PageNumberPagination):
    page_size = 3
