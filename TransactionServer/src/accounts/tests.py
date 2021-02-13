from django.test import TestCase
import json
import requests

# Create your tests here.

# Find the user account we want to update
params = {"userId" : userId}
resp3 = requests.get('http://localhost:8000/api/accounts/', params=params)
account = resp3.json()[0]
triggerId = trigger["id"]

# Update trigger record
account["balance"] = cash
resp4 = requests.put(f'http://localhost:8000/api/account/{userId}/', json=account)
##TODO: update transaction list
print(f"Response after updating trigger with trigger point for ABC stock: {resp4.json()}")