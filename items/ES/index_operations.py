from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from django.http import HttpResponse

es = Elasticsearch()
c = IndicesClient(es)

def del_index(request):
    c.delete('bidding')
    return HttpResponse("index Deleted")

def get_map(request):
    s = c.get_mapping(index='bidding')
    a = c.get_mapping(index='bidding', doc_type='item')

    #print s
    print "\n", a
    return HttpResponse("index Mapped")