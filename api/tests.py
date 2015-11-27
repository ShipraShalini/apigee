from django.test import TestCase
from django.test import Client

c = Client()
c.post('/users/', {'name': 'fred', 'email': 'secret@abc.in'})
