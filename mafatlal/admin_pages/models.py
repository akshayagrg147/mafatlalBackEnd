from django.db import models


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

    class Meta:
        managed = False
        db_table = 'tbl_subcategories'
        
        
class TblProducts(models.Model):
    product_name = models.CharField(max_length=75)
    product_category = models.ForeignKey(TblCategories, models.DO_NOTHING, db_column='product_category', blank=True, null=True)
    product_sub_category = models.ForeignKey(TblSubcategories, models.DO_NOTHING, db_column='product_sub_category', blank=True, null=True)
    price = models.CharField(max_length=10,blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    product_image = models.CharField(max_length=1000, blank=True, null=True)
    size_available = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_on = models.DateTimeField()
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_on = models.DateTimeField()
    updated_by = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_products'
        

        
        