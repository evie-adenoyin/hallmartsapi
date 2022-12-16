from rest_framework.pagination import LimitOffsetPagination


class ProductListLimitOffsetPagination(LimitOffsetPagination):
    default_limit =16
    # max_limit = 0