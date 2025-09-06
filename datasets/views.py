from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count, Min, Max
from .models import Sales ,CSVUploadLog
from .serializers import SalesSerializer 
from .pagination import SalesPagination
from django.db.models import Sum, DecimalField, IntegerField
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import pandas as pd
import os
from django.conf import settings
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SalesListView(generics.ListAPIView):
    queryset = Sales.objects.all().order_by("id")
    serializer_class = SalesSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SalesPagination

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of all sales records. "
                              "This endpoint requires authentication. "
                              "Use `page` query parameter for pagination.",
        manual_parameters=[
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number for pagination (default is 1)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Number of items per page (default is 20)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],
        responses={
            200: openapi.Response(
                description="Paginated list of sales records",
                examples={
                    "application/json": {
                        "count": 100,
                        "next": "http://127.0.0.1:8000/api/sales/?page=2",
                        "previous": None,
                        "results": [
                            {
                                "id": 1,
                                "order_id": "ORD-1001",
                                "amount": "150.00",
                                "order_date": "2025-09-01",
                                "ship_city": "Mumbai",
                                "ship_state": "Maharashtra",
                                "ship_country": "India"
                            },
                            {
                                "id": 2,
                                "order_id": "ORD-1002",
                                "amount": "200.00",
                                "order_date": "2025-09-02",
                                "ship_city": "Pune",
                                "ship_state": "Maharashtra",
                                "ship_country": "India"
                            }
                        ]
                    }
                }
            ),
            401: openapi.Response(description="Authentication credentials were not provided or are invalid."),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        GET /api/sales/
        Retrieve a paginated list of all sales records.
        """
        return super().get(request, *args, **kwargs)


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

    results = [
        {"date": item["order_date"], "total_sales": float(item["total_sales"])}
        for item in data
    ]

    return Response(results)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])  
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

    else: 
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



@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def upload_csv_file(request):
    file_obj = request.FILES.get("file")
    if not file_obj:
        return Response({"error": "No file provided"}, status=400)
    if not file_obj.name.endswith(".csv"):
        return Response({"error": "File must be CSV"}, status=400)

    upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file_obj.name)

    with open(file_path, "wb+") as f:
        for chunk in file_obj.chunks():
            f.write(chunk)

    try:
        df = pd.read_csv(file_path)
        row_count = len(df)
    except Exception as e:
        return Response({"error": f"Failed to read CSV: {str(e)}"}, status=400)

    CSVUploadLog.objects.create(
        user=request.user,
        file_name=file_obj.name,
        row_count=row_count
    )

    return Response({
        "message": "File uploaded successfully",
        "file_name": file_obj.name,
        "row_count": row_count
    })




@swagger_auto_schema(
    method='get',
    operation_description="Retrieve all CSV upload logs, including file name, row count, uploaded by which user, and upload timestamp.",
    responses={
        200: openapi.Response(
            description="List of CSV upload logs",
            examples={
                "application/json": [
                    {
                        "file_name": "sales_data_2025.csv",
                        "row_count": 150,
                        "user": "john_doe",
                        "upload_time": "2025-09-06 12:34:56"
                    },
                    {
                        "file_name": "sales_data_2024.csv",
                        "row_count": 200,
                        "user": "jane_smith",
                        "upload_time": "2025-08-30 10:20:15"
                    }
                ]
            }
        ),
        401: "Unauthorized - Authentication credentials were not provided."
    }
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def csv_upload_logs(request):
    logs = CSVUploadLog.objects.all().order_by("-upload_time")
    data = [
        {
            "file_name": log.file_name,
            "row_count": log.row_count,
            "user": log.user.username,
            "upload_time": log.upload_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for log in logs
    ]
    return Response(data)