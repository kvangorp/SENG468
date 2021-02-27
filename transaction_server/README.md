# Transaction Server

## API Endpoints

This server has an endpoint for each user command. Each endpoint accepts POST requests and expects the body of the request to contain the specified parameters in JSON format.

| User Command | Endpoint | Expected Data |
| --- | --- | --- |
| ADD | /api/commands/add/ | userId, amount |
| QUOTE | /api/commands/quote/ | userId, stockSymbol |
| BUY | /api/commands/buy/ | userId, stockSymbol, amount |
| COMMIT_BUY | /api/commands/commit_buy/ | userId |
| CANCEL_BUY | /api/commands/cancel_buy/ | userId |
| SELL | /api/commands/sell/ | userId, stockSymbol, amount |
| COMMIT_SELL | /api/commands/commit_sell/ | userId |
| CANCEL_SELL | /api/commands/cancel_sell/ | userId |
| SET_BUY_AMOUNT | /api/commands/set_buy_amount/ | userId, stockSymbol, amount |
| SET_BUY_TRIGGER | /api/commands/set_buy_trigger/ | userId, stockSymbol, amount |
| CANCEL_SET_BUY | /api/commands/cancel_set_buy/ | userId, stockSymbol |
| SET_SELL_AMOUNT | /api/commands/set_sell_amount/ | userId, stockSymbol, amount |
| SET_SELL_TRIGGER | /api/commands/set_sell_trigger/ | userId, stockSymbol, amount |
| CANCEL_SET_SELL | /api/commands/cancel_set_sell/ | userId, stockSymbol |
| DUMPLOG | /api/transactions/ | userId (optional) |
| DISPLAY_SUMMARY | /api/commands/display_summary/ | userId |


## Running the server on its own
- To start up the server, run the following commands while in the transaction_server directory:

```
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt

cd src
python manage.py migrate
python manage.py runserver
```
