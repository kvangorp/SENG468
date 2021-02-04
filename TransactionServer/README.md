# API Endpoints

| User Commands | HTTP Method | Endpoint |
| --- | --- | --- |
| ADD | PUT | /api/accounts/{userId}/ |
| QUOTE | GET | /api/quotes/{stockSymbol}/user/{userId} |
| COMMIT BUY, COMMIT SELL | PUT | /api/stocks/{stockSymbol}/user/{userId} |
| COMMIT BUY TRIGGER, COMMIT SELL TRIGGER | POST | /api/triggers/{stockSymbol}/user/{userId} |
