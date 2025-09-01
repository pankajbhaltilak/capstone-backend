from django.urls import path
from .views import SalesListView, SalesSchemaView, SalesSummaryView

urlpatterns = [
    path("sales/", SalesListView.as_view(), name="sales-list"),
    path("sales/schema/", SalesSchemaView.as_view(), name="sales-schema"),
    path("sales/summary/", SalesSummaryView.as_view(), name="sales-summary"),
]
