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



class SalesListView(generics.ListAPIView):
    queryset = Sales.objects.all().order_by("id")  # ensures consistent order
    serializer_class = SalesSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SalesPagination


class SalesSchemaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        schema = {field.name: field.get_internal_type() for field in Sales._meta.get_fields()}
        return Response(schema)


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
 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sales_by_region(request):
    level = request.GET.get("level", "state") 
    qs = Sales.objects.all()

    if level == "country":
        data = qs.values("ship_country").annotate(
            total_orders=Count("id"),
            total_sales=Sum("amount")
        )
        result = [{"region": d["ship_country"], "total_orders": d["total_orders"], "total_sales": d["total_sales"]} for d in data]

    elif level == "city":
        data = qs.values("ship_city").annotate(
            total_orders=Count("id"),
            total_sales=Sum("amount")
        )
        result = [{"region": d["ship_city"], "total_orders": d["total_orders"], "total_sales": d["total_sales"]} for d in data]

    else:  # state
        data = qs.values("ship_state").annotate(
            total_orders=Count("id"),
            total_sales=Sum("amount")
        )
        result = [{"region": d["ship_state"], "total_orders": d["total_orders"], "total_sales": d["total_sales"]} for d in data]

    return Response(result)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def top_cities(request):
    limit = int(request.GET.get("limit", 10))
    qs = Sales.objects.all()

    # Optional date filtering
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    if start_date:
        qs = qs.filter(order_date__gte=start_date)
    if end_date:
        qs = qs.filter(order_date__lte=end_date)

    data = qs.values("ship_city", "ship_state").annotate(
        orders=Count("id")
    ).order_by("-orders")[:limit]

    result = [{"city": d["ship_city"], "state": d["ship_state"], "orders": d["orders"]} for d in data]
    return Response(result)