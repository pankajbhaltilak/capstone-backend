from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count, Min, Max
from .models import Sales
from .serializers import SalesSerializer
from .pagination import SalesPagination


# ✅ Get paginated list of sales
class SalesListView(generics.ListAPIView):
    queryset = Sales.objects.all().order_by("id")  # ensures consistent order
    serializer_class = SalesSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SalesPagination


# ✅ Get schema info
class SalesSchemaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        schema = {field.name: field.get_internal_type() for field in Sales._meta.get_fields()}
        return Response(schema)


# ✅ Get dataset summary
class SalesSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stats = Sales.objects.aggregate(
            total_orders=Count("id"),
            total_sales=Sum("amount"),
            min_date=Min("order_date"),
            max_date=Max("order_date"),
        )
        return Response(stats)


