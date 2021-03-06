from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


CATS = (
    ('Toys', 'Toys'),
    ('Animals', 'Animals'),
    ('Furniture', 'Furniture'),
    ('Food', 'Food'),
    ('Other', 'Other'),
)

class User(AbstractUser):
    pass

class listing(models.Model):
    ownerid = models.IntegerField()
    listingname = models.CharField(max_length=64)
    initialvalue = models.DecimalField(decimal_places=2, max_digits=4000000)
    winnerid = models.IntegerField(null = True, blank=True, default=None)
    description = models.CharField(max_length=200)
    imgurl = models.URLField()
    active = models.BooleanField()
    category = models.CharField(choices=CATS, default='Toys', max_length=9)

class bids(models.Model):
    listingid = models.IntegerField()
    userid = models.IntegerField()
    value = models.DecimalField(decimal_places=2, max_digits=4000000)
    date = models.DateTimeField

class comments(models.Model):
    listingid = models.IntegerField()
    userid = models.IntegerField()
    username = models.CharField(max_length=64)
    date = models.DateTimeField
    comment = models.CharField(max_length=600)

class watchlist(models.Model):
    listingid = models.IntegerField()
    watcherid = models.IntegerField()
    active = models.BooleanField()
