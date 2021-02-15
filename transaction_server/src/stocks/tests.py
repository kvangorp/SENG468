from django.test import TestCase
import json
import requests

# SET UP: ADD SOME MONEY TO USER ACCOUNT
acct = {
    'userId': '1',
    'balance': '1000.00',
}
resp1 = requests.post('http://localhost:8000/api/accounts/', data=acct)
print(f"Response after adding money to account: {resp1.json()}")

stock_p = {
    'userId': '1',
    'stockSymbol': 'GME',
    'shares': '3'
}
resp2 = requests.post('http://localhost:8000/api/stocks/', data=stock_p)
print(f"Response after adding GME stock: {resp2.json()}")

stock_g = {
    'userId': '1',
    'stockSymbol': 'GME',
}
resp3 = requests.get('http://localhost:8000/api/stocks/', data=stock_g)
print(f"Response after getting GME stock: {resp3.json()}")
