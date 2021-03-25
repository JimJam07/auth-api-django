from django.db import models


class User(models.Model):
    name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=20)
    dob = models.CharField(max_length=10,default="01/01/2000")
    phoneNumber = models.IntegerField(default=99999999)


# SELECT sobjects.name FROM sysobjects sobjects WHERE sobjects.xtype = 'U';