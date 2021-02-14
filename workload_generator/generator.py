import requests

file1 = open('1userWorkLoad.txt', 'r')
Lines = file1.readlines()

def generateCommand(line):
    command = line[0]
    print(command)
    commandSwitch(line)
    print("done")

def commandSwitch(command):
	#IF COMMAND MATCHES, CALL THE FUNCTION FOR THE COMMAND, WITH THE PARAMETERS 
	#AS SHOWN AT https://www.ece.uvic.ca/~seng468/ProjectWebSite/Commands.html
	#PARAMETERS SHOULD BE IN ORDER, AND BE ACCESSED BY command[1],....
    
    if command[0] == 'ADD':
        add(command[1], command[2])
    elif command[0] == 'QUOTE': 
        quote(command[1], command[2])
	# elif command == 'BUY':
	# elif command == 'COMMIT_BUY':
	# elif command == 'CANCEL_BUY':
	# elif command == 'SELL':
	# elif command == 'COMMIT_SELL':
	# elif command == 'CANCEL_SELL':
	# elif command == 'SET_BUY_AMOUNT':
	# elif command == 'CANCEL_SET_BUY':
	# elif command == 'SET_BUY_TRIGGER':
	# elif command == 'SET_SELL_AMOUNT':
	# elif command == 'SET_SELL_TRIGGER':
	# elif command == 'CANCEL_SET_SELL':
	# elif command == 'DUMPLOG':
	# elif command == 'DUMPLOG':
	# elif command == 'DISPLAY_SUMMARY':
	

def add(userid,amount):
    data = {
        'userId': userid
    }
    res = requests.get('http://localhost:8000/api/accounts/', params=data)
    print(res)
    account = res.json()[0]
    resId = account['id']
    print(resId)
    account['balance'] += float(amount)
    print(account)
    res1 = requests.put(f'http://localhost:8000/api/accounts/{resId}/', json=account)
    print(res1)
    
def quote(userid, stock):
    res = requests.get(f'http://localhost:8000/api/quotes/{userid}/{stock}/')
    print(res)
    quote = res.json()['quote']
    timestamp = res.json()['timestamp']
    cryptokey = res.json()['cryptokey']
    print(quote)

for line in Lines:
    fileLine = line.split(' ')
    commandLine = fileLine[1]
    generateCommand(commandLine.split(','))
    