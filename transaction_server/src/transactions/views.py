from django.shortcuts import render
from rest_framework import mixins, generics
from .serializers import TransactionSerializer
from .models import Transactions
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class TransactionView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = TransactionSerializer
    queryset = Transactions.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['userId', 'userCommand']

    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)