from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class listing(models.Model):
    ownerid = models.IntegerField()
    listingname = models.CharField(max_length=64)
    initialvalue = models.DecimalField(decimal_places=2, max_digits=9)
    enddate = models.DateTimeField

class bids(models.Model):
    listingid = models.IntegerField()
    userid = models.IntegerField()
    value = models.DecimalField(decimal_places=2, max_digits=9)
    date = models.DateTimeField


class comments(models.Model):
    listingid = models.IntegerField()
    userid = models.IntegerField()
    date = models.DateTimeField
    comment = models.CharField(max_length=200)

