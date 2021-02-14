from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework import generics, status, mixins
from .serializers import AccountSerializer
from .models import Account
from rest_framework.response import Response
from django.http import Http404

class AccountListView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['userId']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class AccountDetailView(generics.GenericAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def get_object(self, pk): #find pk's useracount
        try:
            return Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk): #return json of pk's useraccount
        account = self.get_object(pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    def put(self, request, pk):
        #account = self.get_object(pk)
        
        userId = request.data.get("userId")
        # Find account
        account = Account.objects.filter(
            userId=userId,
        ).first()

        if account is None:
            account = Account(
                userId=userId,
                password='hey',
                balance=0.0,
                pending=0.0,
            )
        # Make sure request can be serialized
        serializer = AccountSerializer(account, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Save updated trigger
        serializer.save()
        return Response(serializer.data)

    # def AddFunds(userId, cash):
    # # Find the user account we want to update
    # params = {"userId" : userId}
    # resp3 = requests.get('http://localhost:8000/api/accounts/', params=params)
    # account = resp3.json()[0]
    # triggerId = trigger["id"]

    # # Update trigger record
    # account["balance"] = cash
    # resp4 = requests.put(f'http://localhost:8000/api/account/{userId}/', json=account)
    # ##update transaction list
    # print(f"Response after updating trigger with trigger point for ABC stock: {resp4.json()}")