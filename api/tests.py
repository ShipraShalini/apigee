from django.test import TestCase
from django.test import Client
from django.test.utils import setup_test_environment
setup_test_environment()

c = Client()

 # get a response from '/'
 #response = client.get('/')
 # we should expect a 404 from that address
 #response.status_code


response =c.post('/users/', {'name': 'fred', 'email': 'secret@abc.in'})

response = c.post('/user_login/', {'name': 'fred', 'password': 'johnpassword'})

response