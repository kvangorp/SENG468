import requests

#get quote data from server
quoteReq = 'S, oY01WVirLr'.encode()
r = requests.get('http://192.168.4.2:4444',params = quoteReq)

elements = r.content.decode().split(',')
 
quoteResult = {
'quote':elements[0],
'stockSymbol':elements[1],
'userID':elements[2],
'timestamp':elements[3],
'cryptokey':elements[4]
}

resp1 = requests.post('http://localhost:8000/api/quotes/', data=quoteResult)
print(f"Response after adding quote: {resp1.json()}")

