from django.db import models

class StockItem(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    detail = models.CharField(max_length=255, null=True, default=None)
    jm_id = models.CharField(max_length=255, null=True, default=None)
    be_id = models.CharField(max_length=255, null=True, default=None)
    unit_price = models.FloatField(default=None, null=True)
    barcode_id = models.CharField(max_length=255, null=True, default=None)
    piece = models.IntegerField(default=0, null=True)
    discounted = models.BooleanField(default=False)
    qt = models.FloatField(default=0.0, null=True)
    cost = models.FloatField(default=0.0, null=True)
    code = models.CharField(max_length=255, null=True, default=None)
    taxactive = models.BooleanField(default=False)