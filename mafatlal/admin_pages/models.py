from django.db import models
from home_screen.models import TblAddress
from login.models import TblUser


class TblState(models.Model):
    state_name = models.CharField(max_length=75)

    class Meta:
        managed = False
        db_table = 'tbl_state'
        
class TblDistrict(models.Model):
    district_name = models.CharField(max_length=75)
    state = models.ForeignKey('TblState', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_district'
        

class TblOrganization(models.Model):
    org_name = models.CharField(max_length=75)
    state = models.ForeignKey('TblState', models.DO_NOTHING, blank=True, null=True)
    district = models.ForeignKey('TblDistrict', models.DO_NOTHING, blank=True, null=True)
    sub = models.ForeignKey('TblSubcategories', models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey('TblCategories', models.DO_NOTHING, db_column='category', blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_organization'
        
class TblCategories(models.Model):
    categories_name = models.CharField(max_length=75)
    state = models.CharField(max_length=75)
    image = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.BigIntegerField(blank=True, null=True)
    updated_by = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_categories'


class TblSubcategories(models.Model):
    subcategories_name = models.CharField(max_length=75)
    category = models.ForeignKey(TblCategories, models.DO_NOTHING, db_column='category')
    image = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.BigIntegerField(blank=True, null=True)
    updated_by = models.BigIntegerField(blank=True, null=True)
    banner_images = models.CharField(max_length=5000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_subcategories'
        
        
class TblProducts(models.Model):
    product_name = models.CharField(max_length=75)
    product_category = models.ForeignKey(TblCategories, models.DO_NOTHING, db_column='product_category', blank=True, null=True)
    product_sub_category = models.ForeignKey(TblSubcategories, models.DO_NOTHING, db_column='product_sub_category', blank=True, null=True)
    price = models.CharField(max_length=10,blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    product_image = models.CharField(max_length=3000, blank=True, null=True)
    size_available = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_on = models.DateTimeField()
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_on = models.DateTimeField()
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    state = models.ForeignKey(TblState, models.DO_NOTHING, db_column='state', blank=True, null=True)
    district = models.ForeignKey(TblDistrict, models.DO_NOTHING, db_column='district', blank=True, null=True)
    organization = models.ForeignKey(TblOrganization, models.DO_NOTHING, db_column='organization', blank=True, null=True)
    gst_percentage = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_products'
        
class TblSubAdmin(models.Model):
    user = models.ForeignKey(TblUser, models.DO_NOTHING)
    role = models.CharField(max_length=500, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    district = models.CharField(max_length=30, blank=True, null=True)
    category = models.CharField(max_length=500, blank=True, null=True)
    sub_category = models.CharField(max_length=500, blank=True, null=True)
    organization = models.CharField(max_length=500, blank=True, null=True)
    gst_number = models.CharField(max_length=100, blank=True, null=True)
    shipping_address = models.ForeignKey(TblAddress, models.DO_NOTHING, db_column='shipping_address', blank=True, null=True, related_name='ship')
    gst_information = models.CharField(max_length=500, blank=True, null=True)
    billing_address = models.ForeignKey(TblAddress, models.DO_NOTHING, db_column='billing_address', blank=True, null=True, related_name='bill')
    created_on = models.DateTimeField()
    created_by = models.CharField(max_length=50)
    updated_on = models.DateTimeField()
    updated_by = models.CharField(max_length=50)
    mobile = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_sub_admin'
        
        