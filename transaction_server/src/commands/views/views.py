from rest_framework.views import APIView

class AddView(APIView):
    def post(self, request):
        print('add')


class QuoteView(APIView):
    def post(self, request):
        print('quote')


class DumplogView(APIView):
    def post(self, request):
        print('dumplog')

class DisplaySummaryView(APIView):
    def post(self, request):
        print('display summary')