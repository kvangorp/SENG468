# API Endpoints

| User Commands | HTTP Method | Enpoint |
| --- | --- | --- |
| ADD | PUT | /api/accounts/{userId}/ |
| QUOTE | GET | /api/quotes/{stockSymbol}/user/{userId} |
| COMMIT BUY, COMMIT SELL | PUT | /api/stocks/{stockSymbol}/user/{userId} |
| COMMIT BUY TRIGGER, COMMIT  | POST | /api/triggers/{stockSymbol}/user/{userId} |