from django.db import models

#map bidders with users
class Items(models.Model):
    item_name = models.CharField(max_length=200, primary_key=True)
    seller = models.CharField(max_length=200, default='')
    date_added = models.DateTimeField()
    image = models.ImageField(upload_to='/home/hypatia/bidengine/image', default='/home/hypatia/Downloads/thumbnail-default.jpg')
    status = models.CharField(max_length=20, default= 'Available')
    min_bid = models.IntegerField(default=0)


class bids(models.Model):
    item = models.ForeignKey(Items)
    bidder = models.CharField(max_length=200)
    bid_amount = models.IntegerField(default=0)
