from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listings(models.Model):
    item_name = models.CharField(max_length=64)
    asking_price = models.IntegerField()
    posting_date = models.DateField()
    category = models.CharField(max_length=64)


class Bids(models.Model):
    bidding_price = models.IntegerField()
    details = models.CharField(max_length=64)


class Comments(models.Model):
    comment_post = models.CharField(max_length=128)
