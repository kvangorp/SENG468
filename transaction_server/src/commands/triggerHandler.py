from .utils import get_quote
from .models import Account, Trigger, Quote, Stock
import time

def triggerHandler():
    while(True):

        # Get list of fully initialized triggers
        triggers = Trigger.objects.all().exclude(triggerPoint=None)
        stocks = triggers.values('stockSymbol').distinct()

        # Iterate through list of stocks used in triggers
        for stock in stocks:
            userId = 'triggerHandler'
            stockSymbol = stock['stockSymbol']

            # Get quote for stock and cache
            quoteResponse = get_quote(userId, stockSymbol)
            quote = quoteResponse.quote

            # Get triggers for the current stock
            currentTriggers = triggers.filter(
                stockSymbol=stockSymbol
            )

            # Iterate through triggers for current stock
            for trigger in currentTriggers:
                if trigger.isBuy and quote <= trigger.triggerPoint:
                    processBuy(trigger, quote)

                elif not trigger.isBuy and quote >= trigger.triggerPoint:
                    processSell(trigger, quote)

        time.sleep(5)

def processBuy(trigger, quote):
    # Get data
    userId = trigger.userId
    stockSymbol = trigger.stockSymbol
    amount = trigger.amount

    # Find user account
    userAccount = Account.objects.filter(
        userId=userId,
    ).first()

    # Find stock account
    stockAccount, created = Stock.objects.get_or_create(
        userId=userId,
        stockSymbol=stockSymbol
    )

    # Calculate shares
    shares = amount/quote

    # Decrement user pending account and add shares to stock account
    userAccount.pending -= amount
    userAccount.save()

    stockAccount.shares += shares
    stockAccount.save()

    # Delete trigger
    trigger.delete()


def processSell(trigger, quote):
    # Get data
    userId = trigger.userId
    stockSymbol = trigger.stockSymbol
    shareAmount = trigger.amount

    # Find user account
    userAccount = Account.objects.filter(
        userId=userId,
    ).first()

    # Find stock account
    stockAccount, created = Stock.objects.get_or_create(
        userId=userId,
        stockSymbol=stockSymbol
    )

    # Calculate price
    dollarAmount = shareAmount*quote

    # Increment user balance and remove shares from reserved stock account
    userAccount.balance += dollarAmount
    userAccount.save()

    stockAccount.reserved -= shareAmount
    stockAccount.save()

    # Delete trigger
    trigger.delete()


        
    
        



