from rest_framework.views import APIView

class SellView(APIView):
    def post(self, request):
        print('sell')


class CommitSellView(APIView):
    def post(self, request):
        print('commit sell')


class CancelSellView(APIView):
    def post(self, request):
        print('cancel sell')