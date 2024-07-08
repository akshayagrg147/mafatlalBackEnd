from django.db import models


class TblUser(models.Model):
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    salt_key = models.CharField(max_length=255)
    is_distributor = models.BooleanField()
    created_on = models.DateTimeField()
    created_by = models.CharField(max_length=50)
    updated_on = models.DateTimeField()
    updated_by = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tbl_user'