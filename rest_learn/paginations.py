from rest_framework import pagination


class GenericPagination(pagination.PageNumberPagination):
    page_size = 3
