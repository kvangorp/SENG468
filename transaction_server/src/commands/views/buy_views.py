from rest_framework.views import APIView

class BuyView(APIView):
    def post(self, request):
        print('buy')


class CommitBuyView(APIView):
    def post(self, request):
        print('commit buy')


class CancelBuyView(APIView):
    def post(self, request):
        print('cancel buy')