# docs.py
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

csv_upload_logs_schema = swagger_auto_schema(
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
