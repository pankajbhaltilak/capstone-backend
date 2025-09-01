from rest_framework.pagination import PageNumberPagination

class SalesPagination(PageNumberPagination):
    page_size = 20  # default 20 per page
    page_size_query_param = "page_size"  # allow client to override
    max_page_size = 100  # limit to avoid huge queries
