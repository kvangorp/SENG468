import requests
from time import time
from database2xml import XMLgen
from lxml import etree

WEBSERVER = 'WS'
file1 = open('./testfiles/1userWorkLoad.txt', 'r')
Lines = file1.readlines()
TRANSACTIONNUM = 0

def user_command_log(userid='', amount=0.0, command='', stockSymbol='', transactionNum=1):
    log = {
        'type': 'userCommand',
        'timestamp': int(time())*1000,
        'server': WEBSERVER,
        'transactionNum': transactionNum,
        'command': command,
        'username': userid,
        'stockSymbol': stockSymbol,
        'funds': amount
    }
    logger = requests.post(f'http://localhost:8080/api/transactions/', json=log)
    print(logger)

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
    elif command[0] == 'SET_BUY_AMOUNT':
        print(command[0])
        set_buy_ammount(command[1], command[2], command[3])
    elif command[0] == 'CANCEL_SET_BUY':
        print(command[0])
        cancel_set_buy(command[1], command[2])
    elif command[0] == 'SET_BUY_TRIGGER':
        print(command[0])
        set_buy_trigger(command[1], command[2], command[3])
    elif command[0] == 'SET_SELL_AMOUNT':
        print(command[0])
        set_sell_ammount(command[1], command[2], command[3])
    elif command[0] == 'SET_SELL_TRIGGER':
        print(command[0])
        set_sell_trigger(command[1], command[2], command[3])
    elif command[0] == 'CANCEL_SET_SELL':
        print(command[0])
        cancel_set_sell(command[1], command[2])
    elif command[0] == 'DUMPLOG':
        print(command[0])
        if len(command) == 3:
            dumplog(command[1], command[2])
        else:
            dumplog(filename=command[1])
    elif command[0] == 'DISPLAY_SUMMARY':
        print(command[0])
        display_summary(command[1])
	

def transaction_num_generator():
    global TRANSACTIONNUM
    TRANSACTIONNUM += 1
    return TRANSACTIONNUM

    
def add(userid, amount):
    transactionNum = transaction_num_generator()
    data = {
        'userId': userid,
        'amount': amount,
        'transactionNum': transactionNum
    }
    user_command_log(userid, amount, 'ADD', transactionNum=transactionNum)
    
    res = requests.post('http://localhost:8080/api/commands/add/', json=data)
    print(res)
   

def quote(userid, stock):
    transactionNum = transaction_num_generator()
    data = {
        'userId': userid,
        'stockSymbol': stock,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid, 0, 'QUOTE', stock, transactionNum=transactionNum)

    res = requests.post('http://localhost:8080/api/commands/quote/', json=data)
    print(res)
   

def buy(userid, stock, dollar_amount):
    transactionNum = transaction_num_generator()
    data = {
        'userId': userid,
        'stockSymbol': stock,
        'amount': dollar_amount,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid, dollar_amount, 'BUY', stock, transactionNum=transactionNum)

    res = requests.post('http://localhost:8080/api/commands/buy/', json=data)
    print(res)
    

#TODO: add status field to buy commands: pending, commited, cancelled
def commit_buy(userid):
    transactionNum = transaction_num_generator()
    data = {
        'userId': userid,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid, 0.0, 'COMMIT_BUY', '', transactionNum=transactionNum) 

    res = requests.post('http://localhost:8080/api/commands/commit_buy/', json=data)
    print(res)
   

def cancel_buy(userid):
    transactionNum = transaction_num_generator()
    data = {
        'userId': userid,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid=userid, command='CANCEL_BUY',transactionNum=transactionNum) 

    res = requests.post('http://localhost:8080/api/commands/cancel_buy/', json=data)
    print(res)
    

def sell(userid, stock, dollar_amount):
    transactionNum = transaction_num_generator()
    data = {
        'userId': userid,
        'stockSymbol': stock,
        'amount': dollar_amount,
        'transactionNum': transactionNum
    
    }
    
    user_command_log(userid, dollar_amount, 'SELL', stock, transactionNum=transactionNum)

    res = requests.post('http://localhost:8080/api/commands/sell/', json=data)
    print(res)
   

def commit_sell(userid):
    transactionNum = transaction_num_generator()
    data = {
        'userId': userid,
        'transactionNum': transactionNum
    }
   
    user_command_log(userid, 0.0, 'COMMIT_SELL', '', transactionNum=transactionNum)

    res = requests.post('http://localhost:8080/api/commands/commit_sell/', json=data)
    print(res)
 

def cancel_sell(userid):
    transactionNum = transaction_num_generator()
    data = {
        'userId': userid,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid=userid, command='CANCEL_SELL', transactionNum=transactionNum)

    res = requests.post('http://localhost:8080/api/commands/cancel_sell/', json=data)
    print(res)
     

def set_buy_ammount(userId, stockSymbol, dollar_amount):
    transactionNum = transaction_num_generator()
    data = {
        'userId': userId,
        'stockSymbol': stockSymbol,
        'amount': dollar_amount,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid=userId, command='SET_BUY_AMOUNT', amount=dollar_amount, transactionNum=transactionNum)

    res = requests.post(f'http://localhost:8080/api/commands/set_buy_amount/', json=data)
    print(res)
    

def cancel_set_buy(userId, stockSymbol):
    transactionNum = transaction_num_generator()
    data = {
        'userId': userId,
        'stockSymbol': stockSymbol,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid=userId, command='CANCEL_SET_BUY',transactionNum=transactionNum)

    res = requests.post(f'http://localhost:8080/api/commands/cancel_set_buy/', json=data)
    print(res)
    

def set_buy_trigger(userId, stockSymbol, dollar_amount):
    transactionNum = transaction_num_generator()
    data = {
        'userId': userId,
        'stockSymbol': stockSymbol,
        'amount': dollar_amount,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid=userId, command='SET_BUY_TRIGGER', amount=dollar_amount, transactionNum=transactionNum)
    
    res = requests.post(f'http://localhost:8080/api/commands/set_buy_trigger/', json=data)
    print(res)
   

def set_sell_ammount(userId, stockSymbol, stock_amount):
    transactionNum = transaction_num_generator()
    data = {
        'userId': userId,
        'stockSymbol': stockSymbol,
        'amount': stock_amount,
        'transactionNum': transactionNum
    }
   
    user_command_log(userid=userId, command='SET_SELL_AMOUNT', amount=stock_amount, transactionNum=transactionNum)

    res = requests.post(f'http://localhost:8080/api/commands/set_sell_amount/', json=data)
    print(res)
    

def set_sell_trigger(userId, stockSymbol, dollar_amount):
    transactionNum = transaction_num_generator()
    data = {
        'userId': userId,
        'stockSymbol': stockSymbol,
        'amount': dollar_amount,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid=userId, command='SET_SELL_TRIGGER', amount=dollar_amount, transactionNum=transactionNum)

    res = requests.post(f'http://localhost:8080/api/commands/set_sell_trigger/', json=data)
    print(res)
   

def cancel_set_sell(userId, stockSymbol):
    transactionNum = transaction_num_generator()
    data = {
        'userId': userId,
        'stockSymbol': stockSymbol,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid=userId, command='CANCEL_SET_SELL',transactionNum=transactionNum)
    
    res = requests.post(f'http://localhost:8080/api/commands/cancel_set_sell/', json=data)
    print(res)
    

def dumplog(userid='', filename=''):
    filename = filename.strip()
    transactionNum = transaction_num_generator()
    user_command_log(userid=userid, command='DUMPLOG', transactionNum=transactionNum)
    if userid:
        data = {
            'userId': userid,
            'transactionNum': transactionNum
        }
        res = requests.post('http://localhost:8080/api/commands/dumplog/', params=data)
    else:
        res = requests.post('http://localhost:8080/api/commands/dumplog/') 
    print(res.json())
    XMLgen.createDocument(filename, res.json())


def display_summary(userId):
    transactionNum = transaction_num_generator()
    data = {
        'userId': userId
    }
    
    user_command_log(userid=userId, command='DISPLAY_SUMMARY', transactionNum=transactionNum)
    res = requests.post(f'http://localhost:8080/api/commands/display_summary/', json=data)
    print(res)
    

for line in Lines:
    fileLine = line.split(' ')
    commandLine = fileLine[1]
    print(fileLine[0])
    commandSwitch(commandLine.split(','))

