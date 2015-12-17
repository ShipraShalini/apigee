from elasticsearch_dsl import DocType, String, Date, Nested, analyzer, Integer

class Item(DocType):
    item_name = String()
    created_at = Date()
    seller = String()
    status = String()
    min_bid = Integer()

    class Meta:
        index='bidding'
        doc_type = 'item'

    # category = String(
    #     analyzer=html_strip,
    #     fields={'raw': String(index='not_analyzed')}
    # )

class bids(DocType):
    item = String() #create relationship
    bidder = String()
    bid_amount = Integer()
