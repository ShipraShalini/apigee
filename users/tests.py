from django.test import TestCase
from django.test import Client
from django.test.utils import setup_test_environment
setup_test_environment()
c = Client()
# response = c.post('/user_login/', {'username': "abc", 'password': 'johnpassword'})
# response.content
# response = c.post('/view_bids/', {'item': "xyz"})
#
#
# response = c.post('/create_bid/', {'item': "xyz", 'amount':85})

#response = c.post('/add_item/', {'name': "a2tt", 'min_bid':85})

#response = c.post('/view_item/', {'name': 'bbb'})

#Add User
response = c.post('/user_add/', {'username': "qffrfrf", 'first_name': "Aaaa", 'last_name':'BBbbb', 'email': 'abc@example.com'})
#login
#response = c.post('/user_login/', {'username': "abc", 'password': 'abc123'})
#response.content
# get a response from '/'
#response = client.get('/')
# we should expect a 404 from that address
#responsestatus_code
'''
{"username": "qffrfrf", "first_name": "Aaaa", "last_name":"BBbbb", "email": "abc@example.com"}

Add bid
{
    "item": "Ferrari",
    "amount" : 733545
}

Add item
{
    "item": "shoe",
    "amount" : 1300
}



user_login
    {
        "username": "brad",
        "password": "johnpassword"
    }

#
# response =c.post('/users/', {'name': 'fred', 'email': 'secret@abc.in'})
#
# response = c.post('/view_item/', {'name': 'bbb'})
# response = c.post('/view_item/', {'name': 'bbb'})
#
#
'''''
