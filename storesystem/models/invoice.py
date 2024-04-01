from django.db import models
from .user_info import *
from .stock_item import *

class Invoice(models.Model):
    customer = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True, default=None)
    status = models.TextField()
    detail = models.CharField(max_length=30, blank=True)
    paid = models.CharField(max_length=30, blank=True)
    totalTax = models.DecimalField(max_digits=65,decimal_places=2)
    totalPrice = models.DecimalField(max_digits=65,decimal_places=2)
    totalDiscounted = models.DecimalField(max_digits=65,decimal_places=2)
    totalPrice = models.DecimalField(max_digits=65,decimal_places=2)
    invoiceNumber = models.TextField()
    credit = models.DecimalField(max_digits=65,decimal_places=2)
    totalProfit = models.DecimalField(max_digits=65,decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    request_date = models.DateTimeField(auto_now_add=True)
    require_date = models.DateTimeField(null=True, default=None)

class InvoiceItems(models.Model):
    inv = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=65,decimal_places=2)
    tax = models.DecimalField(max_digits=65,decimal_places=2)