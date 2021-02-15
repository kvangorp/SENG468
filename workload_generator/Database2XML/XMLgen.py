import sys
from lxml import etree

def userCommandsGen(input):
    commandType = etree.Element("userCommand") 
        
    timestamp = etree.SubElement(commandType, "timestamp") 
    timestamp.text = input['timestamp'] 

    server = etree.SubElement(commandType, "server") 
    server.text = input['server']

    transactionNum = etree.SubElement(commandType, "transactionNum") 
    transactionNum.text = input['transNum']

    command = etree.SubElement(commandType, "command") 
    command.text = input['cmd']

    username = etree.SubElement(commandType, "username") 
    username.text = input['user']

    stockSymbol = etree.SubElement(commandType, "stockSymbol") 
    stockSymbol.text = input['stock']

    filename = etree.SubElement(commandType, "filename") 
    filename.text = input['file']

    funds = etree.SubElement(commandType, "funds") 
    funds.text = input['funds']

    return commandType

def quoteServerGen(input):
    quoteServer = etree.Element("quoteServer")
    
    timestamp = etree.SubElement(quoteServer, "timestamp") 
    timestamp.text = input['timestamp']

    server = etree.SubElement(quoteServer, "server") 
    server.text = input['server']

    transactionNum = etree.SubElement(quoteServer, "transactionNum") 
    transactionNum.text = input['transNum']

    price = etree.SubElement(quoteServer, "price") 
    price.text = input['price']

    stockSymbol = etree.SubElement(quoteServer, "stockSymbol") 
    stockSymbol.text = input['stockSymbol']

    username = etree.SubElement(quoteServer, "username") 
    username.text = input['user']

    quoteServerTime = etree.SubElement(quoteServer, "quoteServerTime") 
    quoteServerTime.text = input['quoteTime']

    cryptokey = etree.SubElement(quoteServer, "cryptokey") 
    cryptokey.text = input['cryptoKey']

    return quoteServer

def userAccountGen(input):
    accountTransaction = etree.Element("accountTransaction")
    
    timestamp = etree.SubElement(accountTransaction, "timestamp") 
    timestamp.text = input['timestamp']

    server = etree.SubElement(accountTransaction, "server") 
    server.text = input['server']

    transactionNum = etree.SubElement(accountTransaction, "transactionNum") 
    transactionNum.text = input['transNum']

    action = etree.SubElement(accountTransaction, "action") 
    action.text = input['userCommand']

    username = etree.SubElement(accountTransaction, "username") 
    username.text = input['user']

    funds = etree.SubElement(accountTransaction, "funds") 
    funds.text = input['amount']

    return accountTransaction

def systemEventGen(input):
    systemEvent = etree.Element("systemEvent")
    
    timestamp = etree.SubElement(systemEvent, "timestamp") 
    timestamp.text = input['timestamp']

    server = etree.SubElement(systemEvent, "server") 
    server.text = input['server']

    transactionNum = etree.SubElement(systemEvent, "transactionNum") 
    transactionNum.text = input['transactionNum']

    command = etree.SubElement(systemEvent, "command") 
    command.text = input['command']

    username = etree.SubElement(systemEvent, "username") 
    username.text = input['username']

    stockSymbol = etree.SubElement(systemEvent, "stockSymbol") 
    stockSymbol.text = input['stockSymbol']

    filename = etree.SubElement(systemEvent, "filename") 
    filename.text = input['filename']

    funds = etree.SubElement(systemEvent, "funds") 
    funds.text = input['funds']

    return etree.ElementTree(systemEvent)

def errorEventGen(input):
    errorEvent = etree.Element("errorEvent")
    
    timestamp = etree.SubElement(errorEvent, "eletimestampment") 
    timestamp.text = input['eletimestampment']

    server = etree.SubElement(errorEvent, "server") 
    server.text = input['server']

    transactionNum = etree.SubElement(errorEvent, "transactionNum") 
    transactionNum.text = input['transactionNum']

    command = etree.SubElement(errorEvent, "command") 
    command.text = input['command']

    username = etree.SubElement(errorEvent, "username") 
    username.text = input['username']

    stockSymbol = etree.SubElement(errorEvent, "stockSymbol") 
    stockSymbol.text = input['stockSymbol']

    filename = etree.SubElement(errorEvent, "filename") 
    filename.text = input['filename']

    funds = etree.SubElement(errorEvent, "funds") 
    funds.text = input['funds']

    errorMessage = etree.SubElement(errorEvent, "errorMessage") 
    errorMessage.text = input['errorMessage']

    return etree.ElementTree(errorEvent)

def debugEventGen(input):
    debugEvent = etree.Element("debugEvent") 
    
    timestamp = etree.SubElement(debugEvent, "timestamp") 
    timestamp.text = input['timestamp']

    server = etree.SubElement(debugEvent, "server") 
    server.text = input['server']

    transactionNum = etree.SubElement(debugEvent, "transactionNum") 
    transactionNum.text = input['transactionNum']

    command = etree.SubElement(debugEvent, "command") 
    command.text = input['command']

    username = etree.SubElement(debugEvent, "username") 
    username.text = input['username']

    stockSymbol = etree.SubElement(debugEvent, "stockSymbol") 
    stockSymbol.text = input['stockSymbol']

    filename = etree.SubElement(debugEvent, "filename") 
    filename.text = input['filename']

    funds = etree.SubElement(debugEvent, "funds") 
    funds.text = input['funds']

    debugMessage = etree.SubElement(debugEvent, "debugMessage") 
    debugMessage.text = input['debugMessage']

    return etree.ElementTree(debugEvent)

def logGen(input):
# log file
    log = etree.Element("log")
    
    userCommand = etree.SubElement(log, "userCommand") 
    userCommand.text = input['userCommand']

    quoteServer = etree.SubElement(log, "quoteServer") 
    quoteServer.text = input['quoteServer']

    accountTransaction = etree.SubElement(log, "accountTransaction") 
    accountTransaction.text = input['accountTransaction']

    systemEvent = etree.SubElement(log, "systemEvent") 
    systemEvent.text = input['systemEvent']

    errorEvent = etree.SubElement(log, "errorEvent") 
    errorEvent.text = input['errorEvent']

    debugEvent = etree.SubElement(log, "debugEvent") 
    debugEvent.text = input['debugEvent']

    return etree.ElementTree(log)

def createDocument(filename, transaction_list):
    log = etree.Element("log")
    for row in transaction_list:
        if row['type'] == 'userCommand':
            input = {
                'timestamp': str(row['timestamp']),
                'server': row['server'],
                'transNum': str(row['transactionNum']),
                'cmd': row['userCommand'],
                'user': row['userId'],
                'stock': row['stockSymbol'],
                'file': filename,
                'funds': str(row['amount'])
            }
            eTree = userCommandsGen(input)
            log.append(eTree)
        elif row['type'] == 'quoteServer':
            input = {
                'timestamp': str(row['timestamp']),
                'server': row['server'],
                'transNum': str(row['transactionNum']),
                'price': str(row['price']),
                'stockSymbol': row['stockSymbol'],
                'user': row['userId'],
                'quoteTime': str(row['quoteServerTime']),
                'cryptoKey': row['cryptoKey']
            }
            eTree = quoteServerGen(input)
            log.append(eTree)
        elif row['type'] == 'accountTransaction':
            input = {
                'timestamp': str(row['timestamp']),
                'server': row['server'],
                'transNum': str(row['transactionNum']),
                'userCommand': row['userCommand'],
                'user': row['userId'],
                'amount': str(row['amount']),
            }
            eTree = userAccountGen(input)
            log.append(eTree)
    tree = etree.ElementTree(log)
    tree.write(filename+'.xml', pretty_print=True, encoding=None, xml_declaration=True)

