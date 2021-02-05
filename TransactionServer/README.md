# API Endpoints

| Assigned | User Commands | HTTP Method | Endpoint |
| --- | --- | --- | --- |
| Connor | ADD | PUT | /api/accounts/{userId}/ |
| Dayton | QUOTE | GET | /api/quotes/{stockSymbol}/user/{userId} |
| Tram | COMMIT BUY, COMMIT SELL | PUT | /api/stocks/{stockSymbol}/user/{userId} |
| Katelyn | SET BUY TRIGGER, CANCEL BUY TRIGGER, SET SELL TRIGGER, CANCEL SELL TRIGGER, SET BUY AMOUNT, CANCEL SET BUY, SET SELL AMOUNT, CANCEL SET SELL  | POST | /api/triggers/{stockSymbol}/user/{userId} |
