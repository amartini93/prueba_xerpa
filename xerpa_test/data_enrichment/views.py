from rest_framework import generics
from .models import Transaction, Category, Commerce, Keyword
from .serializers import (
    TransactionSerializer,
    CategorySerializer,
    CommerceSerializer,
    KeywordSerializer,
)

# Transaction views
class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

# Category views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Commerce views
class CommerceListCreateView(generics.ListCreateAPIView):
    queryset = Commerce.objects.all()
    serializer_class = CommerceSerializer

class CommerceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Commerce.objects.all()
    serializer_class = CommerceSerializer

# Keyword views
class KeywordListCreateView(generics.ListCreateAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

class KeywordRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
