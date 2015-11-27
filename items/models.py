from django.db import models


class Items(models.Model):
    Name = models.CharField(max_length=200)
    date_added = models.DateTimeField('date added')
    image = models.ImageField()
    time_left =   models.DateTimeField('time left')


class bids(models.Model):
    item = models.ForeignKey(Items)
    bidder = models.CharField(max_length=200)
    bid_amount = models.IntegerField()
