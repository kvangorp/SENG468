from rest_framework.views import APIView

class QuoteView(APIView):
    def post(self, request):
        print('quote')