from django.db import models

#map bidders with users
class Items(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    seller = models.CharField(max_length=200)
    date_added = models.DateTimeField('date added')
    image = models.ImageField()
    status = models.CharField(max_length=20, default= 'Available')
    min_bid = models.IntegerField()


class bids(models.Model):
    item = models.ForeignKey(Items)
    bidder = models.CharField(max_length=200)
    bid_amount = models.IntegerField()




