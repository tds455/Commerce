from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class listing(models.Model):
    userid = models.IntegerField()
    listingname = models.CharField(max_length=64)
    value = models.DecimalField(decimal_places=2)
    enddate = models.DateTimeField

class bids(models.Model):
    pass

class comments(models.Model):
    pass

