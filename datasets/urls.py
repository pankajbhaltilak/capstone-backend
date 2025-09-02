from django.urls import path
from .views import *

urlpatterns = [
    path("sales/", SalesListView.as_view(), name="sales-list"),
    path("sales/schema/", SalesSchemaView.as_view(), name="sales-schema"),
    path("sales/summary/", SalesSummaryView.as_view(), name="sales-summary"),
    path("analytics/kpi/", SalesKPISummary.as_view(), name="sales-kpi"),
    path("sales-trend/", sales_trend, name="sales-trend"),
    path("sales-by-category/", sales_by_category, name="sales-by-category"),
    path("orders-by-status/", orders_by_status, name="orders-by-status"),

]
