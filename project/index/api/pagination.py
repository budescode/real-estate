from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
    )


class PostLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 30

class PostNumberPagination(PageNumberPagination):
    page_size = 2
