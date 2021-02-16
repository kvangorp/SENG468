from rest_framework.views import APIView

class SetSellAmountView(APIView):
    def post(self, request):
        print('set sell amount')

class SetSellTriggerView(APIView):
    def post(self, request):
        print('set sell trigger')

class CancelSetSellView(APIView):
    def post(self, request):
        print('cancel set sell')