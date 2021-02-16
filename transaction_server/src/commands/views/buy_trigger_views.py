from rest_framework.views import APIView

class SetBuyAmountView(APIView):
    def post(self, request):
        print('set buy amount')

class SetBuyTriggerView(APIView):
    def post(self, request):
        print('set buy trigger')

class CancelSetBuyView(APIView):
    def post(self, request):
        print('cancel set buy')