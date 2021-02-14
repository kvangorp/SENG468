import sys
from lxml import etree

def userCommandsGen(input):
    commandType = etree.Element("userCommand") #xsd:complexType
        
    timestamp = etree.SubElement(commandType, "timestamp") #xsd:element
    timestamp.text = input['timestamp'] 

    server = etree.SubElement(commandType, "server") #xsd:element
    server.text = input['server']

    transactionNum = etree.SubElement(commandType, "transactionNum") #xsd:element
    transactionNum.text = input['transNum']

    command = etree.SubElement(commandType, "command") #xsd:element
    command.text = input['cmd']

    username = etree.SubElement(commandType, "username") #xsd:element
    username.text = input['user']

    stockSymbol = etree.SubElement(commandType, "stockSymbol") #xsd:element
    stockSymbol.text = input['stock']

    filename = etree.SubElement(commandType, "filename") #xsd:element
    filename.text = input['file']

    funds = etree.SubElement(commandType, "funds") #xsd:element
    funds.text = input['funds']

    return etree.ElementTree(commandType)

def quoteServerGen():
    complexType = etree.Element("complexType") #xsd:complexType
    complexType.set("name", "QuoteServerType")
    
    all1 = etree.SubElement(complexType, "all") #xsd:all
    
    timestamp = etree.SubElement(all1, "element") #xsd:element
    timestamp.set("name", "timestamp")
    timestamp.set("type", "unixTimeLimits")

    server = etree.SubElement(all1, "element") #xsd:element
    server.set("name", "server")
    server.set("type", "xsd:string")

    transactionNum = etree.SubElement(all1, "element") #xsd:element
    transactionNum.set("name", "transactionNum")
    transactionNum.set("type", "xsd:positiveInteger")

    price = etree.SubElement(all1, "element") #xsd:element
    price.set("name", "price")
    price.set("type", "xsd:decimal")

    stockSymbol = etree.SubElement(all1, "element") #xsd:element
    stockSymbol.set("name", "stockSymbol")
    stockSymbol.set("type", "stockSymbolType")

    username = etree.SubElement(all1, "element") #xsd:element
    username.set("name", "username")
    username.set("type", "xsd:string")

    quoteServerTime = etree.SubElement(all1, "element") #xsd:element
    quoteServerTime.set("name", "quoteServerTime")
    quoteServerTime.set("type", "xsd:integer")

    cryptokey = etree.SubElement(all1, "element") #xsd:element
    cryptokey.set("name", "cryptokey")
    cryptokey.set("type", "xsd:string")

    return etree.ElementTree(complexType)

def userAccountGen():
    complexType = etree.Element("complexType") #xsd:complexType
    complexType.set("name", "AccountTransactionType")
    
    all1 = etree.SubElement(complexType, "all") #xsd:all
    
    timestamp = etree.SubElement(all1, "element") #xsd:element
    timestamp.set("name", "timestamp")
    timestamp.set("type", "unixTimeLimits")

    server = etree.SubElement(all1, "element") #xsd:element
    server.set("name", "server")
    server.set("type", "xsd:string")

    transactionNum = etree.SubElement(all1, "element") #xsd:element
    transactionNum.set("name", "transactionNum")
    transactionNum.set("type", "xsd:positiveInteger")

    action = etree.SubElement(all1, "element") #xsd:element
    action.set("name", "action")
    action.set("type", "xsd:string")

    username = etree.SubElement(all1, "element") #xsd:element
    username.set("name", "username")
    username.set("type", "xsd:string")

    funds = etree.SubElement(all1, "element") #xsd:element
    funds.set("name", "funds")
    funds.set("type", "xsd:decimal")

    return etree.ElementTree(complexType)

def systemEventGen():
    complexType = etree.Element("complexType") #xsd:complexType
    complexType.set("name", "SystemEventType")
    
    all1 = etree.SubElement(complexType, "all") #xsd:all
    
    timestamp = etree.SubElement(all1, "element") #xsd:element
    timestamp.set("name", "timestamp")
    timestamp.set("type", "unixTimeLimits")

    server = etree.SubElement(all1, "element") #xsd:element
    server.set("name", "server")
    server.set("type", "xsd:string")

    transactionNum = etree.SubElement(all1, "element") #xsd:element
    transactionNum.set("name", "transactionNum")
    transactionNum.set("type", "xsd:positiveInteger")

    command = etree.SubElement(all1, "element") #xsd:element
    command.set("name", "command")
    command.set("type", "commandType")

    username = etree.SubElement(all1, "element") #xsd:element
    username.set("name", "username")
    username.set("type", "xsd:string")

    stockSymbol = etree.SubElement(all1, "element") #xsd:element
    stockSymbol.set("name", "stockSymbol")
    stockSymbol.set("type", "stockSymbolType")

    filename = etree.SubElement(all1, "element") #xsd:element
    filename.set("name", "filename")
    filename.set("type", "xsd:string")

    funds = etree.SubElement(all1, "element") #xsd:element
    funds.set("name", "funds")
    funds.set("type", "xsd:decimal")

    return etree.ElementTree(complexType)

def errorEventGen():
    complexType = etree.Element("complexType") #xsd:complexType
    complexType.set("name", "ErrorEventType")
    
    all1 = etree.SubElement(complexType, "all") #xsd:all
    
    timestamp = etree.SubElement(all1, "element") #xsd:element
    timestamp.set("name", "timestamp")
    timestamp.set("type", "unixTimeLimits")

    server = etree.SubElement(all1, "element") #xsd:element
    server.set("name", "server")
    server.set("type", "xsd:string")

    transactionNum = etree.SubElement(all1, "element") #xsd:element
    transactionNum.set("name", "transactionNum")
    transactionNum.set("type", "xsd:positiveInteger")

    command = etree.SubElement(all1, "element") #xsd:element
    command.set("name", "command")
    command.set("type", "commandType")

    username = etree.SubElement(all1, "element") #xsd:element
    username.set("name", "username")
    username.set("type", "xsd:string")
    username.set("minOccurs", "0")

    stockSymbol = etree.SubElement(all1, "element") #xsd:element
    stockSymbol.set("name", "stockSymbol")
    stockSymbol.set("type", "stockSymbolType")
    stockSymbol.set("minOccurs", "0")

    filename = etree.SubElement(all1, "element") #xsd:element
    filename.set("name", "filename")
    filename.set("type", "xsd:string")
    filename.set("minOccurs", "0")

    funds = etree.SubElement(all1, "element") #xsd:element
    funds.set("name", "funds")
    funds.set("type", "xsd:decimal")
    funds.set("minOccurs", "0")

    errorMessage = etree.SubElement(all1, "element") #xsd:element
    errorMessage.set("name", "errorMessage")
    errorMessage.set("type", "xsd:string")
    errorMessage.set("minOccurs", "0")

    return etree.ElementTree(complexType)

def debugEventGen():
    complexType = etree.Element("complexType") #xsd:complexType
    complexType.set("name", "DebugType")
    
    all1 = etree.SubElement(complexType, "all") #xsd:all
    
    timestamp = etree.SubElement(all1, "element") #xsd:element
    timestamp.set("name", "timestamp")
    timestamp.set("type", "unixTimeLimits")

    server = etree.SubElement(all1, "element") #xsd:element
    server.set("name", "server")
    server.set("type", "xsd:string")

    transactionNum = etree.SubElement(all1, "element") #xsd:element
    transactionNum.set("name", "transactionNum")
    transactionNum.set("type", "xsd:positiveInteger")

    command = etree.SubElement(all1, "element") #xsd:element
    command.set("name", "command")
    command.set("type", "commandType")

    username = etree.SubElement(all1, "element") #xsd:element
    username.set("name", "username")
    username.set("type", "xsd:string")
    username.set("minOccurs", "0")

    stockSymbol = etree.SubElement(all1, "element") #xsd:element
    stockSymbol.set("name", "stockSymbol")
    stockSymbol.set("type", "stockSymbolType")
    stockSymbol.set("minOccurs", "0")

    filename = etree.SubElement(all1, "element") #xsd:element
    filename.set("name", "filename")
    filename.set("type", "xsd:string")
    filename.set("minOccurs", "0")

    funds = etree.SubElement(all1, "element") #xsd:element
    funds.set("name", "funds")
    funds.set("type", "xsd:decimal")
    funds.set("minOccurs", "0")

    debugMessage = etree.SubElement(all1, "element") #xsd:element
    debugMessage.set("name", "debugMessage")
    debugMessage.set("type", "xsd:string")
    debugMessage.set("minOccurs", "0")

    return etree.ElementTree(complexType)

def logGen():
# log file
    complexType = etree.Element("complexType") #xsd:complexType
    complexType.set("name", "LogType")
    
    choice = etree.SubElement(complexType, "choice") #xsd:choice
    choice.set("minOccurs", "0")
    choice.set("maxOccurs", "unbounded")
    
    userCommand = etree.SubElement(choice, "element") #xsd:element
    userCommand.set("name", "userCommand")
    userCommand.set("type", "UserCommandType")

    quoteServer = etree.SubElement(choice, "element") #xsd:element
    quoteServer.set("name", "quoteServer")
    quoteServer.set("type", "QuoteServerType")

    accountTransaction = etree.SubElement(choice, "element") #xsd:element
    accountTransaction.set("name", "accountTransaction")
    accountTransaction.set("type", "AccountTransactionType")

    systemEvent = etree.SubElement(choice, "element") #xsd:element
    systemEvent.set("name", "systemEvent")
    systemEvent.set("type", "SystemEventType")

    errorEvent = etree.SubElement(choice, "element") #xsd:element
    errorEvent.set("name", "errorEvent")
    errorEvent.set("type", "ErrorEventType")

    debugEvent = etree.SubElement(choice, "element") #xsd:element
    debugEvent.set("name", "debugEvent")
    debugEvent.set("type", "DebugType")

    return etree.ElementTree(complexType)

# pretty string
logGen().write('testPrint.xml', pretty_print=True)
