from django.urls import path
from .views import *

urlpatterns = [
    path("sales/", SalesListView.as_view(), name="sales-list"),
    path("sales/summary/", SalesSummaryView.as_view(), name="sales-summary"),
    path("analytics/kpi/", SalesKPISummary.as_view(), name="sales-kpi"),
    path("sales-trend/", sales_trend, name="sales-trend"),
    path("sales-by-category/", sales_by_category, name="sales-by-category"),
    path("orders-by-status/", orders_by_status, name="orders-by-status"),
    path('sales/region/', sales_by_region, name='sales-by-region'),
    path('sales/top-cities/', top_cities, name='top-cities'),
    path("upload-csv/", upload_csv_file, name="upload-csv-file"),
    path("csv-upload-logs/", csv_upload_logs, name="csv-upload-logs"),
]
