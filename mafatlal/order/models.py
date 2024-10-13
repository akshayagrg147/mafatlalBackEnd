from django.db import models
from home_screen.models import TblAddress

# Create your models here.
class TblOrder(models.Model):
    product_quantity = models.IntegerField(blank=True, null=True)
    user_id = models.BigIntegerField()
    price = models.CharField(max_length=10, blank=True, null=True)
    product_image = models.CharField(max_length=3000, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    order_details = models.CharField(max_length=100, blank=True, null=True)
    size_available = models.CharField(max_length=100, blank=True, null=True)
    order_status = models.CharField(max_length=30, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    tracking_url = models.CharField(max_length=100, blank=True, null=True)
    shipping_address = models.ForeignKey(TblAddress, models.DO_NOTHING, db_column='shipping_address', blank=True, null=True, related_name='shipping')
    billing_address = models.ForeignKey(TblAddress, models.DO_NOTHING, db_column='billing_address', blank=True, null=True, related_name='billing')
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_order'