import json
import requests


# SET UP: ADD SOME STOCKS TO USER ACCOUNT
stock = {
    'userId': '1',
    'stockSymbol': 'ABC',
    'shares': '100'
}
resp1 = requests.post('http://localhost:8000/api/stocks/', data=stock)
print(f"Response after adding ABC stock: {resp1.json()}")


# COMMAND: SET SELL AMOUNT (userId: 1, stockSymbol: ABC, amount: 5)
triggerSellAmount = {
    'userId': '1',
    'stockSymbol': 'ABC',
    'shares': '5',
    'isBuy': 'false'
}
resp2 = requests.post('http://localhost:8000/api/triggers/', json=triggerSellAmount)
print(f"Response after adding trigger with sell amount for ABC stock: {resp2.json()}")



# COMMAND: SET SELL TRIGGER (userId: 1, stockSymbol: ABC, amount: 10.00)

# Find the trigger record we want to update
params = {"userId" : "1", "stockSymbol" : "ABC"}
resp3 = requests.get('http://localhost:8000/api/triggers/', params=params)
trigger = resp3.json()[0]
triggerId = trigger["id"]

# Update trigger record
trigger["triggerPoint"] = 10.00
print(trigger)
resp4 = requests.put(f'http://localhost:8000/api/triggers/{triggerId}/', json=trigger)
print(f"Response after updating trigger with trigger point for ABC stock: {resp4.json()}")


# COMMAND: CANCEL SET SELL (userId: 1, stockSymbol: ABC)

# Find the trigger record we want to update
params = {"userId" : "1", "stockSymbol" : "ABC"}
resp5 = requests.get('http://localhost:8000/api/triggers/', params=params)
trigger = resp5.json()[0]
triggerId = trigger["id"]

# Delete the trigger
resp6 = requests.delete(f'http://localhost:8000/api/triggers/{triggerId}/')
print(f"Response after deleting trigger for ABC stock: {resp6.status_code}")