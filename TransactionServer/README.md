# API Endpoints

| User Commands | HTTP Method | Endpoint |
| --- | --- | --- |
| ADD | PUT | /api/accounts/{userId}/ |
| QUOTE | GET | /api/quotes/{stockSymbol}/user/{userId} |
| COMMIT BUY, COMMIT SELL | PUT | /api/stocks/{stockSymbol}/user/{userId} |
| SET BUY TRIGGER, CANCEL BUY TRIGGER, SET SELL TRIGGER, CANCEL SELL TRIGGER, SET BUY AMOUNT, CANCEL SET BUY, SET SELL AMOUNT, CANCEL SELL AMOUNT  | POST | /api/triggers/{stockSymbol}/user/{userId} |
