from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count, Min, Max
from .models import Sales
from .serializers import SalesSerializer
from .pagination import SalesPagination
from django.db.models import Sum, DecimalField, IntegerField
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes



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
    
def parse_bool(val: str | None):
    if val is None:
        return None
    return str(val).lower() in {"1", "true", "yes", "y", "t"}


class SalesKPISummary(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_sales_amount = Sales.objects.aggregate(
            total=Sum("amount", output_field=DecimalField())
        )["total"] or 0

        total_orders = Sales.objects.count()

        total_qty = Sales.objects.aggregate(
            qty=Sum("qty", output_field=IntegerField())
        )["qty"] or 0

        return Response({
            "total_sales_amount": total_sales_amount,
            "total_orders": total_orders,
            "total_qty": total_qty,
        })


@api_view(["GET"])
@permission_classes([IsAuthenticated]) 
def sales_trend(request):
    data = (
        Sales.objects
        .values("order_date")
        .annotate(total_sales=Sum("amount"))
        .order_by("order_date")
    )

    # Format response
    results = [
        {"date": item["order_date"], "total_sales": float(item["total_sales"])}
        for item in data
    ]

    return Response(results)

@api_view(["GET"])
@permission_classes([IsAuthenticated])  # 🔒 JWT protected
def sales_by_category(request):
    data = (
        Sales.objects
        .values("category")
        .annotate(total_sales=Sum("amount"))
        .order_by("-total_sales")
    )

    results = [
        {"category": item["category"] or "Unknown", "total_sales": float(item["total_sales"])}
        for item in data
    ]

    return Response(results)

@api_view(["GET"])
@permission_classes([IsAuthenticated])  # 🔒 JWT protected
def orders_by_status(request):

    
    data = (
        Sales.objects
        .values("status")
        .annotate(order_count=Count("id"))
        .order_by("-order_count")
    )

    results = [
        {"status": item["status"] or "Unknown", "order_count": item["order_count"]}
        for item in data
    ]

    return Response(results)