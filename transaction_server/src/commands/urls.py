from django.urls import path
from .views.views import *
from .views.buy_views import *
from .views.sell_views import *
from .views.buy_triggers import *
from .views.sell_triggers import *

urlpatterns = [

    # Basic Commands
    path('commands/add/', AddView.as_view()),
    path('commands/quote/', QuoteView.as_view()),

    # Buy
    path('commands/buy/', BuyView.as_view()),
    path('commands/commit_buy/', CommitBuyView.as_view()),
    path('commands/cancel_buy/', CancelBuyView.as_view()),

    # Sell
    path('commands/sell/', SellView.as_view()),
    path('commands/commit_sell/', CommitSellView.as_view()),
    path('commands/cancel_sell/', CancelSellView.as_view()),

    # Buy Trigger
    path('commands/set_buy_amount/', SetBuyAmountView.as_view()),
    path('commands/set_buy_trigger/', SetBuyTriggerView.as_view()),
    path('commands/cancel_set_buy/', CancelSetBuyView.as_view()),

    # Sell Trigger
    path('commands/set_sell_amount/', SetSellAmountView.as_view()),
    path('commands/set_sell_trigger/', SetSellTriggerView.as_view()),
    path('commands/cancel_set_sell/', CancelSetSellView.as_view()),

    # Retrieve info
    path('commands/dumplog/', DumplogView.as_view()),
    path('commands/display_summary/', DisplaySummaryView.as_view()),
]