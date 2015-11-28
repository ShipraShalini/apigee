from django.db import models


class Items(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    date_added = models.DateTimeField('date added')
    image = models.ImageField()
    #min_bid = models.IntegerField()


class bids(models.Model):
    item = models.ForeignKey(Items)
    bidder = models.CharField(max_length=200)
    bid_amount = models.IntegerField()




