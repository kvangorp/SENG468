file1 = open('workload.txt', 'r')
Lines = file1.readlines()

def generateCommand(line):
	command = line[0]	
	print(command)

def commandSwitch(command):
	#IF COMMAND MATCHES, CALL THE FUNCTION FOR THE COMMAND, WITH THE PARAMETERS 
	#AS SHOWN AT https://www.ece.uvic.ca/~seng468/ProjectWebSite/Commands.html
	#PARAMETERS SHOULD BE IN ORDER, AND BE ACCESSED BY command[1],....

	if command == 'ADD': add(userid, amount)
	elif command == 'QUOTE':
	elif command == 'BUY':
	elif command == 'COMMIT_BUY':
	elif command == 'CANCEL_BUY':
	elif command == 'SELL':
	elif command == 'COMMIT_SELL':
	elif command == 'CANCEL_SELL':
	elif command == 'SET_BUY_AMOUNT':
	elif command == 'CANCEL_SET_BUY':
	elif command == 'SET_BUY_TRIGGER':
	elif command == 'SET_SELL_AMOUNT':
	elif command == 'SET_SELL_TRIGGER':
	elif command == 'CANCEL_SET_SELL':
	elif command == 'DUMPLOG':
	elif command == 'DUMPLOG':
	elif command == 'DISPLAY_SUMMARY':
	

	
	
	
	

for line in Lines:
	fileLine = line.split(' ')
	commandLine = fileLine[1]
	generateCommand(commandLine.split(','))