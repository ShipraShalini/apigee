from django.test import TestCase
from django.test import Client
from django.test.utils import setup_test_environment
setup_test_environment()
c = Client()
response = c.post('/view_item/', {'name': 'bbb'})

#Add User
#response = c.post('/user_add/', {'username': "abc", 'first_name': "Aaaa", 'last_name':'BBbbb', 'email': 'abc@example.com','password': 'abc123'})

#login
#response = c.post('/user_login/', {'username': "abc", 'password': 'abc123'})
response.content
 # get a response from '/'
 #response = client.get('/')
 # we should expect a 404 from that address
 #response.status_code


response =c.post('/users/', {'name': 'fred', 'email': 'secret@abc.in'})

response = c.post('/view_item/', {'name': 'bbb'})
response = c.post('/view_item/', {'name': 'bbb'})

response