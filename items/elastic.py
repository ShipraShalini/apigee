from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

es = Elasticsearch()

s = Search(es)



def add_doc(index, type, doc):
    res = es.create(index=index, doc_type= type, body=doc)
    return (res['created'])

def del_doc(index, type, doc):
    pass
    #find delete_by_query

def search_index(index, field , value ):
    return s.query("match", field = value)


