import axios from "axios";

export function commandLogger(userid='', amount=0.0, command='', stockSymbol='', transactionNum=1) {
    var request = {
        'type': 'userCommand',
        'timestamp': (new Date()).getTime(),
        'server': 'WS',
        'transactionNum': transactionNum,
        'command': command,
        'username': userid,
        'stockSymbol': stockSymbol,
        'funds': amount
    }
    axios.post('http://localhost:8080/api/transactions/', request)
    .then((response) => {
    console.log(response);
    }) 
}

export function errorLogger (userid='', command='', transactionNum=1) {
    var request = {
        "type": "errorEvent",
        "timestamp": (new Date()).getTime(),
        "server": 'WS',
        "transactionNum": transactionNum,
        "command": command,
        "username": userid,
        "errorMessage": "Error while processing command."
    }
    axios.post('http://localhost:8080/api/transactions/', request)
    .then((response) => {
    console.log(response);
    }) 
}