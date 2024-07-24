from django.db import models
from home_screen.models import TblProducts

# Create your models here.
class TblOrder(models.Model):
    product = models.ForeignKey(TblProducts, models.DO_NOTHING)
    product_quantity = models.IntegerField(blank=True, null=True)
    user_id = models.BigIntegerField()
    price = models.CharField(max_length=10, blank=True, null=True)
    product_image = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    order_details = models.TextField(blank=True, null=True)  # This field type is a guess.
    size_available = models.TextField(blank=True, null=True)  # This field type is a guess.
    order_status = models.CharField(max_length=30, blank=True, null=True)
    delievery_address = models.CharField(max_length=30)
    delievery_state = models.CharField(max_length=30)
    delievery_pincode = models.BigIntegerField()
    created_on = models.DateTimeField()
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_on = models.DateTimeField()
    updated_by = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_order'