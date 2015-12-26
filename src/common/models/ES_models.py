from elasticsearch_dsl import DocType, String, Date, Integer


class Items(DocType):
    item_name = String(index='not_analyzed')
    created_at = Date(format = "E MMM d H:m:s Y")
    seller = String(index='not_analyzed')
    status = String(index='not_analyzed')
    min_bid = Integer()
    sold_to = String(index='not_analyzed')

    class Meta:
        index='bidding'
        doc_type = 'item'


class Bids(DocType):
    item = String(index='not_analyzed') #create relationship
    bidder = String(index='not_analyzed')
    bid_amount = Integer()


    class Meta:
        index='bidding'
        doc_type = 'bid'
        #parent = 'item'

