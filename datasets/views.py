from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count, Min, Max
from .models import Sales ,CSVUploadLog
from .serializers import SalesSerializer 
from .pagination import SalesPagination
from django.db.models import Sum, DecimalField, IntegerField
from django.db.models.functions import Coalesce
from django.http import JsonResponse
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
from .docs import *
import logging

logger = logging.getLogger(__name__)

def health_check(request):
    return JsonResponse({"status": "ok", "message": "Backend is running"}, status=200)

class SalesListView(generics.ListAPIView):
    queryset = Sales.objects.all().order_by("id")
    serializer_class = SalesSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SalesPagination

def parse_bool(val: str | None):
    if val is None:
        return None
    return str(val).lower() in {"1", "true", "yes", "y", "t"}

class SalesSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            stats = Sales.objects.aggregate(
                total_orders=Count("id"),
                total_sales=Sum("amount"),
                min_date=Min("order_date"),
                max_date=Max("order_date"),
            )

            result = {
                "total_orders": stats.get("total_orders", 0),
                "total_sales": float(stats.get("total_sales") or 0),
                "min_date": stats.get("min_date").strftime("%Y-%m-%d") if stats.get("min_date") else None,
                "max_date": stats.get("max_date").strftime("%Y-%m-%d") if stats.get("max_date") else None,
            }

            return Response(result, status=200)

        except Exception as e:
            logger.error(f"Error in SalesSummaryView: {str(e)}", exc_info=True)
            return Response({"error": "Failed to fetch sales summary."}, status=500)

class SalesKPISummary(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            total_sales_amount = Sales.objects.aggregate(
                total=Sum("amount", output_field=DecimalField())
            )["total"] or Decimal("0.00")

            total_orders = Sales.objects.count()

            total_qty = Sales.objects.aggregate(
                qty=Sum("qty", output_field=IntegerField())
            )["qty"] or 0

            avg_order_value = float(total_sales_amount) / total_orders if total_orders > 0 else 0

            return Response({
                "total_sales_amount": float(total_sales_amount),
                "total_orders": total_orders,
                "total_qty": total_qty,
                "avg_order_value": round(avg_order_value, 2),
            }, status=200)

        except Exception as e:
            logger.error(f"Error in SalesKPISummary: {str(e)}", exc_info=True)

            return Response(
                {"error": "An error occurred while calculating KPIs."},
                status=500
            )
        

@sales_trend_docs
@api_view(["GET"])
@permission_classes([IsAuthenticated]) 
def sales_trend(request):
    try:
        data = (
            Sales.objects
            .values("order_date")
            .annotate(total_sales=Sum("amount"))
            .order_by("order_date")
        )

        results = [
            {
                "date": item["order_date"].strftime("%Y-%m-%d") if item["order_date"] else "Unknown",
                "total_sales": float(item["total_sales"]) if item["total_sales"] else 0.0
            }
            for item in data
        ]

        return Response(results, status=200)

    except Exception as e:
        logger.error(f"Error in sales_trend: {str(e)}", exc_info=True)
        return Response(
            {"error": "An error occurred while fetching sales trend data."},
            status=500
        )
    

@sales_by_category_docs
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def sales_by_category(request):
    try:
        data = (
            Sales.objects
            .values("category")
            .annotate(total_sales=Sum("amount"))
            .order_by("-total_sales")
        )

        results = [
            {
                "category": item["category"] if item["category"] else "Unknown",
                "total_sales": float(item["total_sales"]) if item["total_sales"] else 0.0
            }
            for item in data
        ]

        return Response(results, status=200)

    except Exception as e:
        logger.error(f"Error in sales_by_category: {str(e)}", exc_info=True)

        return Response(
            {"error": "An error occurred while fetching sales by category."},
            status=500
        )


@orders_by_status_docs
@api_view(["GET"])
@permission_classes([IsAuthenticated])  
def orders_by_status(request):
    try:
        data = (
            Sales.objects
            .values("status")
            .annotate(order_count=Count("id"))
            .order_by("-order_count")
        )
        results = [
            {
                "status": item["status"] if item["status"] else "Unknown",
                "order_count": item["order_count"]
            }
            for item in data
        ]
        return Response(results, status=200)

    except Exception as e:
        logger.error(f"Error in orders_by_status view: {str(e)}", exc_info=True)

        return Response(
            {"error": "Something went wrong while fetching orders by status."},
            status=500
        )   

@sales_by_region_docs
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sales_by_region(request):
    try:
        level = request.GET.get("level", "state")
        qs = Sales.objects.all()

        if level == "country":
            data = qs.values("ship_country").annotate(
                total_orders=Count("id"),
                total_sales=Sum("amount")
            )
            result = [
                {
                    "region": d["ship_country"],
                    "total_orders": d["total_orders"],
                    "total_sales": float(d["total_sales"] or 0)
                }
                for d in data
            ]

        elif level == "city":
            data = qs.values("ship_city").annotate(
                total_orders=Count("id"),
                total_sales=Sum("amount")
            )
            result = [
                {
                    "region": d["ship_city"],
                    "total_orders": d["total_orders"],
                    "total_sales": float(d["total_sales"] or 0)
                }
                for d in data
            ]

        else:  
            data = qs.values("ship_state").annotate(
                total_orders=Count("id"),
                total_sales=Sum("amount")
            )
            result = [
                {
                    "region": d["ship_state"],
                    "total_orders": d["total_orders"],
                    "total_sales": float(d["total_sales"] or 0)
                }
                for d in data
            ]

        return Response(result, status=200)

    except Exception as e:
        logger.error(f"Error in sales_by_region view: {str(e)}", exc_info=True)
        return Response(
            {"error": "Something went wrong while fetching sales by region."},
            status=500
        )

@top_cities_docs
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def top_cities(request):
    try:
        limit = int(request.GET.get("limit", 10))
        qs = Sales.objects.all()

        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        if start_date:
            qs = qs.filter(order_date__gte=start_date)
        if end_date:
            qs = qs.filter(order_date__lte=end_date)

        data = qs.values("ship_city", "ship_state").annotate(
            orders=Count("id")
        ).order_by("-orders")[:limit]

        result = [
            {"city": d["ship_city"], "state": d["ship_state"], "orders": d["orders"]}
            for d in data
        ]

        return Response(result, status=200)

    except Exception as e:
        logger.error(f"Error in top_cities view: {str(e)}", exc_info=True)
        return Response({"error": "Something went wrong while fetching top cities"}, status=500)


@csv_upload_docs
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def upload_csv_file(request):
    try:
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"error": "No file provided"}, status=400)

        if not file_obj.name.lower().endswith(".csv"):
            return Response({"error": "File must be in CSV format"}, status=400)

        # 3. Ensure upload directory exists
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
            logger.error(f"Error reading CSV file {file_obj.name}: {str(e)}", exc_info=True)
            return Response({"error": f"Failed to read CSV: {str(e)}"}, status=400)

        # Save log in database
        CSVUploadLog.objects.create(
            user=request.user,
            file_name=file_obj.name,
            row_count=row_count
        )

        return Response({
            "message": "File uploaded successfully",
            "file_name": file_obj.name,
            "row_count": row_count
        }, status=201)

    except Exception as e:
        logger.error(f"Unexpected error in upload_csv_file: {str(e)}", exc_info=True)
        return Response(
            {"error": "An unexpected error occurred while uploading the file."},
            status=500
        )



@csv_upload_logs_docs
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def csv_upload_logs(request):
    try:
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

        return Response(data, status=200)

    except Exception as e:
        logger.error(f"Error in csv_upload_logs: {str(e)}", exc_info=True)

        return Response(
            {"error": "Something went wrong while fetching the logs."},
            status=500
        )
