from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

csv_upload_docs = swagger_auto_schema(
    method='post',
    operation_description="Upload a CSV file and log the upload details.",
    manual_parameters=[
        openapi.Parameter(
            name='file',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            description='CSV file to upload',
            required=True
        ),
    ],
    responses={
        200: openapi.Response(
            description="File uploaded successfully",
            examples={
                "application/json": {
                    "message": "File uploaded successfully",
                    "file_name": "sales_data.csv",
                    "row_count": 120
                }
            }
        ),
        400: openapi.Response(
            description="Invalid request",
            examples={
                "application/json": {"error": "File must be CSV"}
            }
        ),
        401: "Unauthorized"
    },
    tags=["CSV Upload"]
)

# CSV Upload Logs Documentation
csv_upload_logs_docs = swagger_auto_schema(
    method='get',
    operation_description=(
        "Retrieve all CSV upload logs.\n\n"
        "Each log contains:\n"
        "- **file_name**: Name of the uploaded CSV file.\n"
        "- **row_count**: Number of rows in the uploaded CSV file.\n"
        "- **user**: Username of the person who uploaded the file.\n"
        "- **upload_time**: Timestamp when the file was uploaded."
    ),
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
        401: openapi.Response(
            description="Unauthorized",
            examples={
                "application/json": {
                    "detail": "Authentication credentials were not provided."
                }
            }
        )
    },
    tags=["CSV Upload"]
)

top_cities_docs = swagger_auto_schema(
    method='get',
    operation_description=(
        "Retrieve a list of top cities by the number of orders.\n\n"
        "**Query Parameters:**\n"
        "- `limit` *(integer, optional)*: Number of top cities to return. Default is `10`.\n"
        "- `start_date` *(string, optional)*: Filter orders from this date (format: YYYY-MM-DD).\n"
        "- `end_date` *(string, optional)*: Filter orders up to this date (format: YYYY-MM-DD).\n\n"
        "**Response:** Returns a list of cities with total orders."
    ),
    manual_parameters=[
        openapi.Parameter(
            'limit',
            openapi.IN_QUERY,
            description="Number of top cities to return (default is 10)",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'start_date',
            openapi.IN_QUERY,
            description="Filter orders from this date (YYYY-MM-DD)",
            type=openapi.TYPE_STRING,
            format='date'
        ),
        openapi.Parameter(
            'end_date',
            openapi.IN_QUERY,
            description="Filter orders up to this date (YYYY-MM-DD)",
            type=openapi.TYPE_STRING,
            format='date'
        ),
    ],
    responses={
        200: openapi.Response(
            description="List of top cities with their order counts",
            examples={
                "application/json": [
                    {"city": "Mumbai", "state": "Maharashtra", "orders": 150},
                    {"city": "Delhi", "state": "Delhi", "orders": 120},
                    {"city": "Bangalore", "state": "Karnataka", "orders": 100}
                ]
            }
        ),
        401: openapi.Response(
            description="Unauthorized",
            examples={
                "application/json": {
                    "detail": "Authentication credentials were not provided."
                }
            }
        )
    },
    tags=["Regional analytics"]
)


sales_by_region_docs = swagger_auto_schema(
    method='get',
    operation_description=(
        "Retrieve aggregated sales data grouped by region.\n\n"
        "**Query Parameters:**\n"
        "- `level` *(string, optional)*: The level of region aggregation. Default is `state`.\n"
        "  - `country` → Group by country\n"
        "  - `state` → Group by state (default)\n"
        "  - `city` → Group by city\n\n"
        "**Response:** Returns a list of regions with total orders and total sales."
    ),
    manual_parameters=[
        openapi.Parameter(
            'level',
            openapi.IN_QUERY,
            description=(
                "Region grouping level:\n"
                "- `country` → Group by country\n"
                "- `state` → Group by state (default)\n"
                "- `city` → Group by city"
            ),
            type=openapi.TYPE_STRING,
            enum=["country", "state", "city"],
            default="state"
        ),
    ],
    responses={
        200: openapi.Response(
            description="List of regions with aggregated total orders and total sales",
            examples={
                "application/json": [
                    {"region": "Maharashtra", "total_orders": 150, "total_sales": 120000.50},
                    {"region": "Karnataka", "total_orders": 100, "total_sales": 95000.00},
                    {"region": "Delhi", "total_orders": 80, "total_sales": 72000.00}
                ]
            }
        ),
        401: openapi.Response(
            description="Unauthorized",
            examples={
                "application/json": {
                    "detail": "Authentication credentials were not provided."
                }
            }
        )
    },
    tags=["Regional analytics"]
)

orders_by_status_docs = swagger_auto_schema(
    method='get',
    operation_description=(
        "Retrieve the count of orders grouped by their status.\n\n"
        "Returns a list of order statuses and the number of orders for each status."
    ),
    responses={
        200: openapi.Response(
            description="List of order statuses with order counts",
            examples={
                "application/json": [
                    {"status": "Shipped - Delivered to Buyer", "order_count": 120},
                    {"status": "Pending", "order_count": 45},
                    {"status": "Cancelled", "order_count": 10},
                    {"status": "Unknown", "order_count": 2}
                ]
            }
        ),
        401: openapi.Response(
            description="Unauthorized",
            examples={
                "application/json": {"detail": "Authentication credentials were not provided."}
            }
        )
    },
    tags=["Sales Analytics"]
)


sales_by_category_docs = swagger_auto_schema(
    method='get',
    operation_description=(
        "Retrieve total sales aggregated by product category.\n\n"
        "Returns a list of categories and the total sales amount for each category."
    ),
    responses={
        200: openapi.Response(
            description="List of categories with total sales",
            examples={
                "application/json": [
                    {"category": "kurta", "total_sales": 25000.50},
                    {"category": "t-shirt", "total_sales": 18000.00},
                    {"category": "jeans", "total_sales": 15000.75},
                    {"category": "Unknown", "total_sales": 500.00}
                ]
            }
        ),
        401: openapi.Response(
            description="Unauthorized",
            examples={
                "application/json": {"detail": "Authentication credentials were not provided."}
            }
        )
    },
    tags=["Sales Analytics"]
)

sales_trend_docs = swagger_auto_schema(
    method='get',
    operation_description=(
        "Retrieve total sales aggregated by order date.\n\n"
        "Returns a list of dates and the corresponding total sales for each date."
    ),
    responses={
        200: openapi.Response(
            description="List of dates with total sales",
            examples={
                "application/json": [
                    {"date": "2025-09-01", "total_sales": 4500.50},
                    {"date": "2025-09-02", "total_sales": 6200.00},
                    {"date": "2025-09-03", "total_sales": 7000.75}
                ]
            }
        ),
        401: openapi.Response(
            description="Unauthorized",
            examples={
                "application/json": {"detail": "Authentication credentials were not provided."}
            }
        )
    },
    tags=["Sales Analytics"]
)

sales_kpi_summary_docs = swagger_auto_schema(
    method='get',
    operation_description=(
        "Retrieve overall KPI summary for sales.\n\n"
        "Returns total sales amount, total number of orders, and total quantity sold."
    ),
    responses={
        200: openapi.Response(
            description="Sales KPI summary",
            examples={
                "application/json": {
                    "total_sales_amount": 125000.50,
                    "total_orders": 320,
                    "total_qty": 850
                }
            }
        ),
        401: openapi.Response(
            description="Unauthorized",
            examples={
                "application/json": {"detail": "Authentication credentials were not provided."}
            }
        )
    },
    tags=["KPI Summary"]
)