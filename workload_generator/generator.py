import requests
from time import time
from database2xml import XMLgen
from lxml import etree
import concurrent.futures

WEBSERVER = 'WS'
TRANSACTIONSERVER = 'TS'
fileName = './testfiles/1000userWorkLoad.txt'

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

def error_command_log(userid='', command='', transactionNum=1):
    log = {
        "type": "errorEvent",
        "timestamp": int(time()*1000),
        "server": TRANSACTIONSERVER,
        "transactionNum": transactionNum,
        "command": command,
        "username": userid,
        "errorMessage": "Invalid number of parameters."
    }
    logger = requests.post(f'http://localhost:8080/api/transactions/', json=log)

def commandSwitch(command):
	#IF COMMAND MATCHES, CALL THE FUNCTION FOR THE COMMAND, WITH THE PARAMETERS 
	#AS SHOWN AT https://www.ece.uvic.ca/~seng468/ProjectWebSite/Commands.html
	#PARAMETERS SHOULD BE IN ORDER, AND BE ACCESSED BY command[1],....
    print(f"{command[0]}: {command[1]}")

    if command[1] == 'ADD':
        if len(command) < 4:
            user_command_log(userid=command[2], command='ADD', transactionNum=command[0])
            error_command_log(userid=command[2], command='ADD', transactionNum=command[0])
            return
        add(command[0], command[2], command[3])

    elif command[1] == 'QUOTE': 
        if len(command) < 4:
            user_command_log(userid=command[2], command='QUOTE', transactionNum=command[0])
            error_command_log(userid=command[2], command='QUOTE', transactionNum=command[0])
            return
        quote(command[0], command[2], command[3])

    elif command[1] == 'BUY':
        if len(command) < 5:
            user_command_log(userid=command[2], command='BUY', transactionNum=command[0])
            error_command_log(userid=command[2], command='BUY', transactionNum=command[0])
            return
        buy(command[0], command[2], command[3], command[4])

    elif command[1] == 'COMMIT_BUY':
        if len(command) < 3:
            user_command_log(userid=command[2], command='COMMIT_BUY', transactionNum=command[0])
            error_command_log(userid=command[2], command='COMMIT_BUY', transactionNum=command[0])
            return
        commit_buy(command[0], command[2])

    elif command[1] == 'CANCEL_BUY':
        if len(command) < 3:
            user_command_log(userid=command[2], command='CANCEL_BUY', transactionNum=command[0])
            error_command_log(userid=command[2], command='CANCEL_BUY', transactionNum=command[0])
            return
        cancel_buy(command[0], command[2])

    elif command[1] == 'SELL':
        if len(command) < 5:
            user_command_log(userid=command[2], command='SELL', transactionNum=command[0])
            error_command_log(userid=command[2], command='SELL', transactionNum=command[0])
            return
        sell(command[0], command[2], command[3], command[4])

    elif command[1] == 'COMMIT_SELL':
        if len(command) < 3:
            user_command_log(userid=command[2], command='COMMIT_SELL', transactionNum=command[0])
            error_command_log(userid=command[2], command='COMMIT_SELL', transactionNum=command[0])
            return
        commit_sell(command[0], command[2])

    elif command[1] == 'CANCEL_SELL':
        if len(command) < 3:
            user_command_log(userid=command[2], command='CANCEL_SELL', transactionNum=command[0])
            error_command_log(userid=command[2], command='CANCEL_SELL', transactionNum=command[0])
            return
        cancel_sell(command[0], command[2])

    elif command[1] == 'SET_BUY_AMOUNT':
        if len(command) < 5:
            user_command_log(userid=command[2], command='SET_BUY_AMOUNT', transactionNum=command[0])
            error_command_log(userid=command[2], command='SET_BUY_AMOUNT', transactionNum=command[0])
            return
        set_buy_ammount(command[0], command[2], command[3], command[4])

    elif command[1] == 'CANCEL_SET_BUY':
        if len(command) < 4:
            user_command_log(userid=command[2], command='CANCEL_SET_BUY', transactionNum=command[0])
            error_command_log(userid=command[2], command='CANCEL_SET_BUY', transactionNum=command[0])
            return
        cancel_set_buy(command[0], command[2], command[3])

    elif command[1] == 'SET_BUY_TRIGGER':
        if len(command) < 5:
            user_command_log(userid=command[2], command='SET_BUY_TRIGGER', transactionNum=command[0])
            error_command_log(userid=command[2], command='SET_BUY_TRIGGER', transactionNum=command[0])
            return
        set_buy_trigger(command[0], command[2], command[3], command[4])

    elif command[1] == 'SET_SELL_AMOUNT':
        if len(command) < 5:
            user_command_log(userid=command[2], command='SET_SELL_AMOUNT', transactionNum=command[0])
            error_command_log(userid=command[2], command='SET_SELL_AMOUNT', transactionNum=command[0])
            return
        set_sell_ammount(command[0], command[2], command[3], command[4])

    elif command[1] == 'SET_SELL_TRIGGER':
        if len(command) < 5:
            user_command_log(userid=command[2], command='SET_SELL_TRIGGER', transactionNum=command[0])
            error_command_log(userid=command[2], command='SET_SELL_TRIGGER', transactionNum=command[0])
            return
        set_sell_trigger(command[0], command[2], command[3], command[4])

    elif command[1] == 'CANCEL_SET_SELL':
        if len(command) < 4:
            user_command_log(userid=command[2], command='CANCEL_SET_SELL', transactionNum=command[0])
            error_command_log(userid=command[2], command='CANCEL_SET_SELL', transactionNum=command[0])
            return
        cancel_set_sell(command[0], command[2], command[3])

    elif command[1] == 'DUMPLOG':
        if len(command) == 4:
            dumplog(command[0], command[2], command[3])
        elif len(command) == 3:
            dumplog(transactionNum=command[0], filename=command[2])
        else:
            user_command_log(userid=command[2], command='DUMPLOG', transactionNum=command[0])
            error_command_log(userid=command[2], command='DUMPLOG', transactionNum=command[0])
            return
        
    elif command[1] == 'DISPLAY_SUMMARY':
        if len(command) < 3:
            user_command_log(userid=command[2], command='DISPLAY_SUMMARY', transactionNum=command[0])
            error_command_log(userid=command[2], command='DISPLAY_SUMMARY', transactionNum=command[0])
            return
        display_summary(command[0], command[2])

    else:
        return
    
def add(transactionNum, userid, amount):  
    data = {
        'userId': userid,
        'amount': amount,
        'transactionNum': transactionNum
    }
    user_command_log(userid, amount, 'ADD', transactionNum=transactionNum)

    res = requests.post('http://localhost:8080/api/commands/add/', json=data)
    print(res.status_code) if not res.status_code in (200, 201, 412) else None
   

def quote(transactionNum, userid, stock):
    data = {
        'userId': userid,
        'stockSymbol': stock,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid, 0, 'QUOTE', stock, transactionNum=transactionNum)

    res = requests.post('http://localhost:8080/api/commands/quote/', json=data)
    print(res.status_code) if not res.status_code in (200, 201, 412) else None
   

def buy(transactionNum, userid, stock, dollar_amount):
    data = {
        'userId': userid,
        'stockSymbol': stock,
        'amount': dollar_amount,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid, dollar_amount, 'BUY', stock, transactionNum=transactionNum)

    res = requests.post('http://localhost:8080/api/commands/buy/', json=data)
    print(res.status_code) if not res.status_code in (200, 201, 412) else None
    

def commit_buy(transactionNum, userid):
    data = {
        'userId': userid,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid, 0.0, 'COMMIT_BUY', '', transactionNum=transactionNum) 

    res = requests.post('http://localhost:8080/api/commands/commit_buy/', json=data)
    print(res.status_code) if not res.status_code in (200, 201, 412) else None
   


def cancel_buy(transactionNum, userid):
    data = {
        'userId': userid,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid=userid, command='CANCEL_BUY',transactionNum=transactionNum) 

    res = requests.post('http://localhost:8080/api/commands/cancel_buy/', json=data)
    print(res.status_code) if not res.status_code in (200, 201, 412) else None
    

def sell(transactionNum, userid, stock, dollar_amount):
    data = {
        'userId': userid,
        'stockSymbol': stock,
        'amount': dollar_amount,
        'transactionNum': transactionNum
    
    }
    
    user_command_log(userid, dollar_amount, 'SELL', stock, transactionNum=transactionNum)

    res = requests.post('http://localhost:8080/api/commands/sell/', json=data)
    print(res.status_code) if not res.status_code in (200, 201, 412) else None
   

def commit_sell(transactionNum, userid):
    data = {
        'userId': userid,
        'transactionNum': transactionNum
    }
   
    user_command_log(userid, 0.0, 'COMMIT_SELL', '', transactionNum=transactionNum)

    res = requests.post('http://localhost:8080/api/commands/commit_sell/', json=data)
    print(res.status_code) if not res.status_code in (200, 201, 412) else None
 

def cancel_sell(transactionNum, userid):
    data = {
        'userId': userid,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid=userid, command='CANCEL_SELL', transactionNum=transactionNum)

    res = requests.post('http://localhost:8080/api/commands/cancel_sell/', json=data)
    print(res.status_code) if not res.status_code in (200, 201, 412) else None
     

def set_buy_ammount(transactionNum, userId, stockSymbol, dollar_amount):
    data = {
        'userId': userId,
        'stockSymbol': stockSymbol,
        'amount': dollar_amount,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid=userId, command='SET_BUY_AMOUNT', amount=dollar_amount, transactionNum=transactionNum)

    res = requests.post(f'http://localhost:8080/api/commands/set_buy_amount/', json=data)
    print(res.status_code) if not res.status_code in (200, 201, 412) else None
    

def cancel_set_buy(transactionNum, userId, stockSymbol):
    data = {
        'userId': userId,
        'stockSymbol': stockSymbol,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid=userId, command='CANCEL_SET_BUY',transactionNum=transactionNum)

    res = requests.post(f'http://localhost:8080/api/commands/cancel_set_buy/', json=data)
    print(res.status_code) if not res.status_code in (200, 201, 412) else None
    

def set_buy_trigger(transactionNum, userId, stockSymbol, dollar_amount):
    data = {
        'userId': userId,
        'stockSymbol': stockSymbol,
        'amount': dollar_amount,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid=userId, command='SET_BUY_TRIGGER', amount=dollar_amount, transactionNum=transactionNum)
    
    res = requests.post(f'http://localhost:8080/api/commands/set_buy_trigger/', json=data)
    print(res.status_code) if not res.status_code in (200, 201, 412) else None
   

def set_sell_ammount(transactionNum, userId, stockSymbol, stock_amount):
    data = {
        'userId': userId,
        'stockSymbol': stockSymbol,
        'amount': stock_amount,
        'transactionNum': transactionNum
    }
   
    user_command_log(userid=userId, command='SET_SELL_AMOUNT', amount=stock_amount, transactionNum=transactionNum)

    res = requests.post(f'http://localhost:8080/api/commands/set_sell_amount/', json=data)
    print(res.status_code) if not res.status_code in (200, 201, 412) else None
    

def set_sell_trigger(transactionNum, userId, stockSymbol, dollar_amount):
    data = {
        'userId': userId,
        'stockSymbol': stockSymbol,
        'amount': dollar_amount,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid=userId, command='SET_SELL_TRIGGER', amount=dollar_amount, transactionNum=transactionNum)

    res = requests.post(f'http://localhost:8080/api/commands/set_sell_trigger/', json=data)
    print(res.status_code) if not res.status_code in (200, 201, 412) else None
   

def cancel_set_sell(transactionNum, userId, stockSymbol):
    data = {
        'userId': userId,
        'stockSymbol': stockSymbol,
        'transactionNum': transactionNum
    }
    
    user_command_log(userid=userId, command='CANCEL_SET_SELL',transactionNum=transactionNum)
    
    res = requests.post(f'http://localhost:8080/api/commands/cancel_set_sell/', json=data)
    print(res.status_code) if not res.status_code in (200, 201, 412) else None
    

def dumplog(transactionNum=0, userid='', filename=''):
    filename = filename.strip()
    user_command_log(userid=userid, command='DUMPLOG', transactionNum=transactionNum)
    if userid:
        data = {
            'userId': userid,
            'transactionNum': transactionNum
        }
        res = requests.post('http://localhost:8080/api/commands/dumplog/', json=data)
    else:
        res = requests.post('http://localhost:8080/api/commands/dumplog/') 
    print(res.json())
    XMLgen.createDocument(filename, res.json())


def display_summary(transactionNum, userId):
    data = {
        'userId': userId
    }
    
    user_command_log(userid=userId, command='DISPLAY_SUMMARY', transactionNum=transactionNum)
    res = requests.post(f'http://localhost:8080/api/commands/display_summary/', json=data)
    print(res.status_code) if not res.status_code in (200, 201, 412) else None

def sortByUser(lines):
    print("Sorting commands by user...")
    userCommands = {}

    for line in lines:
        # Parse file line
        parsedCommand = parseLine(line)
        
        # Append command to list of user's commands
        userId = parsedCommand[2]
        userCommands.setdefault(userId, []).append(parsedCommand)

    return userCommands

def parseLine(line):
    # Parse command
    fileLine = line.split(' ')
    commandLine = fileLine[1]
    parsedCommand = commandLine.split(',')

    # Add transaction number to command
    transactionNum = fileLine[0].strip("[]")
    parsedCommand.insert(0, transactionNum)
    return parsedCommand

def handleUserCommands(commands):
    for command in commands:
        commandSwitch(command)


def main():
    # Open and read workload file
    workLoadFile = open(fileName, 'r')
    lines = workLoadFile.readlines()

    commandLines = lines[:len(lines)-1]
    dumplogLine = lines[len(lines)-1]

    # Sort commands by user
    commandsByUser = sortByUser(commandLines)
    numUsers = len(commandsByUser)

    # Set up a thread for each user
    with concurrent.futures.ThreadPoolExecutor(max_workers=numUsers) as executor:
        executor.map(handleUserCommands, commandsByUser.values())

    # Run dumplog
    dumplogCommand = parseLine(dumplogLine)
    commandSwitch(dumplogCommand)



if __name__ == "__main__":
    main()

