import requests
from time import time
from database2xml import XMLgen
from lxml import etree

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
        print(command[0])
        sell(command[1], command[2], command[3]) #userId, symbol, dollaramount
    elif command[0] == 'COMMIT_SELL':
        print(command[0])
        commit_sell(command[1])
    elif command[0] == 'CANCEL_SELL':
        print(command[0])
        cancel_sell(command[1])
	# elif command == 'SET_BUY_AMOUNT':
	# elif command == 'CANCEL_SET_BUY':
	# elif command == 'SET_BUY_TRIGGER':
	# elif command == 'SET_SELL_AMOUNT':
	# elif command == 'SET_SELL_TRIGGER':
	# elif command == 'CANCEL_SET_SELL':
    elif command[0] == 'DUMPLOG':
        print(command[0])
        dumplog(command[1])
	# elif command == 'DUMPLOG':
	# elif command == 'DISPLAY_SUMMARY':
	

def add(userid, amount):
    data = {
        'userId': userid,
        'amount': amount
    }
    res = requests.post('http://localhost:8000/api/commands/add/', json=data)
    print(res)
    # user_command_log(userid, amount, 'ADD')

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

def commit_checker(userid, command):
    data = {
        'userId': userid,
        'userCommand': command
    }
    res = requests.get('http://localhost:8000/api/transactions/', params=data)
    print(res)
    list_of_transactions = res.json()
    print(list_of_transactions)
    latest_command = sorted(list_of_transactions, key=lambda k: k['timestamp'], reverse=True)
    command_time = ''
    if list_of_transactions:
        command_time = float(latest_command[0]['timestamp'])
        stock = latest_command[0]['stockSymbol']
        amount = latest_command[0]['amount']
    else:
        return

    data = {
        'userId': userid,
        'userCommand': 'COMMIT_' + command
    }
    res1 = requests.get('http://localhost:8000/api/transactions/', params=data)
    print(res1)
    list_of_transactions1 = res1.json()
    print(list_of_transactions1)
    latest_commit_command = sorted(list_of_transactions1, key=lambda k: k['timestamp'], reverse=True)
    commit_time = ''
    if list_of_transactions1:
        commit_time = float(latest_commit_command[0]['timestamp'])

    data = {
        'userId': userid,
        'userCommand': 'CANCEL_' + command
    }
    res2 = requests.get('http://localhost:8000/api/transactions/', params=data)
    print(res2)
    list_of_transactions2 = res2.json()
    print(list_of_transactions2)
    latest_cancel_command = sorted(list_of_transactions2, key=lambda k: k['timestamp'], reverse=True)
    cancel_time = ''
    if list_of_transactions2:
        cancel_time = float(latest_cancel_command[0]['timestamp'])
    flag1 = False
    if not commit_time:
        flag1 = True
    elif command_time < commit_time:
        flag1 = True
    else:
        flag1 = False
    flag2 = False
    if not cancel_time:
        flag2 = True
    elif command_time < cancel_time:
        flag2 = True
    else:
        flag2 = False
    is_committable = flag1 and flag2 and ((time() - command_time) <= 60.0)
    return is_committable, stock, amount

#TODO: add status field to buy commands: pending, commited, cancelled
def commit_buy(userid):
    is_committable, stock, amount = commit_checker(userid, 'BUY')
    if is_committable:
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
        print("you have enough shares to sell")
        user_command_log(userid, amount, 'SELL', stock)

def commit_sell(userid):
    is_committable, stock, amount = commit_checker(userid, 'SELL')
    if is_committable:
        stock_quote = quote(userid, stock)
        shares = amount/stock_quote
        data = {
            'userId': userid,
            'stockSymbol': stock,
            'shares': shares,
            'amount': amount
        }
        print(data)
        res = requests.put(f'http://localhost:8000/api/stocks/sell/{userid}/{stock}/', json=data)
        print(res.json)
    user_command_log(userid, amount, 'COMMIT_SELL', stock)

def cancel_sell(userid):
    data = {
        'userId': userid,
        'userCommand': 'SELL'
    }
    res = requests.get('http://localhost:8000/api/transactions/', params=data)
    print(res)
    list_of_transactions = res.json()
    print(list_of_transactions)
    latest_sell = sorted(list_of_transactions, key=lambda k: k['timestamp'], reverse=True)
    sell_time = ''
    if list_of_transactions:
        sell_time = float(latest_sell[0]['timestamp'])
    else:
        return
    if (time() - sell_time) <= 60.0:
        user_command_log(userid=userid, command='CANCEL_SELL')

def dumplog(filename):
    filename = filename.strip()
    res = requests.get('http://localhost:8000/api/transactions/')
    XMLgen.createDocument(filename, res.json())
    

for line in Lines:
    fileLine = line.split(' ')
    commandLine = fileLine[1]
    generateCommand(commandLine.split(','))

