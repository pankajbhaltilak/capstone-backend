from django.db import models

class Sales(models.Model):
    order_id = models.CharField(max_length=50)
    order_date = models.DateField()
    status = models.CharField(max_length=50, null=True, blank=True)
    fulfilment = models.CharField(max_length=50, null=True, blank=True)
    sales_channel = models.CharField(max_length=50, null=True, blank=True)
    ship_service_level = models.CharField(max_length=50, null=True, blank=True)
    style = models.CharField(max_length=100, null=True, blank=True)
    sku = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    asin = models.CharField(max_length=50, null=True, blank=True)
    courier_status = models.CharField(max_length=50, null=True, blank=True)
    qty = models.IntegerField()
    currency = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    ship_city = models.CharField(max_length=100, null=True, blank=True)
    ship_state = models.CharField(max_length=100, null=True, blank=True)
    ship_postal_code = models.CharField(max_length=20, null=True, blank=True)
    ship_country = models.CharField(max_length=50, null=True, blank=True)
    promotion_ids = models.TextField(null=True, blank=True)
    b2b = models.BooleanField(default=False)
    fulfilled_by = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "sales"  # maps to your existing table
