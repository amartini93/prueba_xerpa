from django.urls import path
from .views import (
    TransactionListCreateView,
    TransactionRetrieveUpdateDestroyView,
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
    CommerceListCreateView,
    CommerceRetrieveUpdateDestroyView,
    KeywordListCreateView,
    KeywordRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<uuid:pk>/', TransactionRetrieveUpdateDestroyView.as_view(), name='transaction-detail'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<uuid:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),

    path('commerces/', CommerceListCreateView.as_view(), name='commerce-list-create'),
    path('commerces/<uuid:pk>/', CommerceRetrieveUpdateDestroyView.as_view(), name='commerce-detail'),

    path('keywords/', KeywordListCreateView.as_view(), name='keyword-list-create'),
    path('keywords/<uuid:pk>/', KeywordRetrieveUpdateDestroyView.as_view(), name='keyword-detail'),
]
