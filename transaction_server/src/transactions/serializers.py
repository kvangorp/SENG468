from rest_framework import serializers
from .models import AccountTransaction, UserCommand, ErrorEvent, QuoteServerTransaction

class AccountTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountTransaction
        fields = '__all__'

class UserCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCommand
        fields = '__all__'

class ErrorEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorEvent
        fields = '__all__'

class QuoteServerTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteServerTransaction
        fields = '__all__'