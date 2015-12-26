from src.common.models.ES_models import Bids, Items
from elasticsearch_dsl.connections import connections

# initializing
connections.create_connection(hosts=['localhost'])
Items.init()
Bids.init()