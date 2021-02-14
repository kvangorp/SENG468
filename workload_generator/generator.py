import requests
from time import time

WEBSERVER = 'WS'
file1 = open('1userWorkLoad.txt', 'r')
Lines = file1.readlines()

def user_command_log(userid='', amount=0.0, command='', stockSymbol=''):
    log = {
        'type': 'userCommand',
        'timestamp': time(),
        'server': WEBSERVER,
        'transactionNum': '1',
        'userCommand': command,
        'stockSymbol': stockSymbol,
        'userId': userid,
        'amount': amount
    }
    logger = requests.post(f'http://localhost:8000/api/transactions/', json=log)
    print(logger.json())

def generateCommand(line):
    command = line[0]
    commandSwitch(line)

def commandSwitch(command):
	#IF COMMAND MATCHES, CALL THE FUNCTION FOR THE COMMAND, WITH THE PARAMETERS 
	#AS SHOWN AT https://www.ece.uvic.ca/~seng468/ProjectWebSite/Commands.html
	#PARAMETERS SHOULD BE IN ORDER, AND BE ACCESSED BY command[1],....

    if command[0] == 'ADD':
        print(command[0])
        add(command[1], command[2])
    elif command[0] == 'QUOTE': 
        print(command[0])
        quote(command[1], command[2])
    elif command[0] == 'BUY':
        print(command[0])
        buy(command[1], command[2], command[3])
    elif command[0] == 'COMMIT_BUY':
        print(command[0])
        commit_buy(command[1])
    elif command[0] == 'CANCEL_BUY':
        print(command[0])
        cancel_buy(command[1])
    elif command[0] == 'SELL':
         sell(command[1], command[2], command[3]) #userId, symbol, dollaramount
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
	

def add(userid, amount):
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
    #log
    user_command_log(userid, amount, 'ADD')

def quote(userid, stock):
    res = requests.get(f'http://localhost:8000/api/quotes/{userid}/{stock}/')
    quote = res.json()['quote']
    timestamp = res.json()['timestamp']
    cryptokey = res.json()['cryptokey']
    #log
    user_command_log(userid, 0, 'QUOTE', stock)
    return quote

def buy(userid, stock, dollar_amount):
    data = {
        'userId': userid
    }
    res = requests.get('http://localhost:8000/api/accounts/', params=data)
    print(res)
    account = res.json()[0]
    #check timestamp in log

    if account['balance'] < float(dollar_amount):
        print("yeah no")
    else:
        user_command_log(userid, dollar_amount, 'BUY', stock)

#TODO: add status field to buy commands: pending, commited, cancelled
def commit_buy(userid):
    data = {
        'userId': userid,
        'userCommand': 'BUY'
    }
    res = requests.get('http://localhost:8000/api/transactions/', params=data)
    print(res)
    list_of_transactions = res.json()
    print(list_of_transactions)
    latest_buy = sorted(list_of_transactions, key=lambda k: k['timestamp'], reverse=True)
    buy_time = ''
    if list_of_transactions:
        buy_time = float(latest_buy[0]['timestamp'])
        stock = latest_buy[0]['stockSymbol']
        amount = latest_buy[0]['amount']
    else:
        return

    data = {
        'userId': userid,
        'userCommand': 'COMMIT_BUY'
    }
    res1 = requests.get('http://localhost:8000/api/transactions/', params=data)
    print(res1)
    list_of_transactions1 = res1.json()
    print(list_of_transactions1)
    latest_commit_buy = sorted(list_of_transactions1, key=lambda k: k['timestamp'], reverse=True)
    commit_time = ''
    if list_of_transactions1:
        commit_time = float(latest_commit_buy[0]['timestamp'])

    data = {
        'userId': userid,
        'userCommand': 'CANCEL_BUY'
    }
    res2 = requests.get('http://localhost:8000/api/transactions/', params=data)
    print(res2)
    list_of_transactions2 = res2.json()
    print(list_of_transactions2)
    latest_cancel_buy = sorted(list_of_transactions2, key=lambda k: k['timestamp'], reverse=True)
    cancel_time = ''
    if list_of_transactions2:
        cancel_time = float(latest_cancel_buy[0]['timestamp'])
    flag1 = False
    if not commit_time:
        flag1 = True
    elif buy_time < commit_time:
        flag1 = True
    else:
        flag1 = False
    flag2 = False
    if not cancel_time:
        flag2 = True
    elif buy_time < cancel_time:
        flag2 = True
    else:
        flag2 = False

    if flag1 and flag2 and ((time() - buy_time) <= 60.0):
        stock_quote = quote(userid, stock)
        shares = amount/stock_quote
        data = {
            'userId': userid,
            'stockSymbol': stock,
            'shares': shares,
            'amount': amount
        }
        print(data)
        res = requests.put(f'http://localhost:8000/api/stocks/buy/{userid}/{stock}/', json=data)
        print(res.json)
    user_command_log(userid, amount, 'COMMIT_BUY', stock)

def cancel_buy(userid):
    data = {
        'userId': userid,
        'userCommand': 'BUY'
    }
    res = requests.get('http://localhost:8000/api/transactions/', params=data)
    print(res)
    list_of_transactions = res.json()
    print(list_of_transactions)
    latest_buy = sorted(list_of_transactions, key=lambda k: k['timestamp'], reverse=True)
    buy_time = ''
    if list_of_transactions:
        buy_time = float(latest_buy[0]['timestamp'])
    else:
        return
    if (time() - buy_time) <= 60.0:
        user_command_log(userid=userid, command='CANCEL_BUY')

def sell(userid, stock, amount):
    res = requests.get(f'http://localhost:8000/api/stocks/sell/{userid}/{stock}/')
    print(res)
    account = res.json()
    print(account)

    stock_quote = quote(userid, stock)
    shares = float(amount)/stock_quote
    

    if account['shares'] < shares:
        print("yeah no")
    else:
        user_command_log(userid, amount, 'SELL', stock)






for line in Lines:
    fileLine = line.split(' ')
    commandLine = fileLine[1]
    generateCommand(commandLine.split(','))

