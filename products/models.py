from django.db import models


# Create your models here.
class Products(models.Model):
    id = models.IntegerField(primary_key=True)
    sku_name = models.CharField(max_length=30)
    sku_category = models.CharField(max_length=30)
    price = models.IntegerField()