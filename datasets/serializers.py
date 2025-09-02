from rest_framework import serializers
from .models import Sales

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = "__all__"

class RegionSalesSerializer(serializers.Serializer):
    region = serializers.CharField()
    total_orders = serializers.IntegerField()
    total_sales = serializers.DecimalField(max_digits=12, decimal_places=2)

class TopCitySerializer(serializers.Serializer):
    city = serializers.CharField()
    state = serializers.CharField()
    orders = serializers.IntegerField()
