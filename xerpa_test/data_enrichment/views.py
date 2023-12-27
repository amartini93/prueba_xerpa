import logging
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Transaction, Category, Commerce, Keyword
from .serializers import (
    TransactionSerializer,
    CategorySerializer,
    CommerceSerializer,
    KeywordSerializer,
)

logger = logging.getLogger()

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

# Enrichment view
class EnrichmentView(APIView):
    def post(self, request, *args, **kwargs):
        # Validate the request (you can add more validation as needed)
        transactions = request.data.get('transactions')

        if not transactions:
            return Response({'error': 'No transactions provided'}, status=status.HTTP_400_BAD_REQUEST)
        elif not isinstance(transactions, list):
            return Response({'error': 'Transactions must be a list'}, status=status.HTTP_400_BAD_REQUEST)
        # Validate that each transaction has the required fields
        for transaction in transactions:
            if 'id' not in transaction:
                return Response({'error': 'Transaction must have an id'}, status=status.HTTP_400_BAD_REQUEST)
            elif 'description' not in transaction:
                return Response({'error': 'Transaction must have a description'}, status=status.HTTP_400_BAD_REQUEST)
            elif 'amount' not in transaction:
                return Response({'error': 'Transaction must have an amount'}, status=status.HTTP_400_BAD_REQUEST)
            elif 'date' not in transaction:
                return Response({'error': 'Transaction must have a date'}, status=status.HTTP_400_BAD_REQUEST)

        # Process transactions and perform enrichment (you'll need to implement this logic)
        enriched_transactions = self.process_enrichment(transactions)

        return Response(enriched_transactions, status=status.HTTP_200_OK)

    def process_enrichment(self, transactions):
        enriched_transactions = []
        categorized_transactions = 0
        identified_commerce_transactions = 0

        for transaction in transactions:
            description = transaction['description']
            amount = transaction['amount']
            date = transaction['date']
            first_word = description.split()[0].lower()

            logging.info(f"Looking for description: {description}")
            logging.info(f"Looking for keyword for the first word: {first_word}")

            keyword = Keyword.objects.filter(keyword__iexact=first_word).first()

            # Initialize the dictionary with null fields
            enriched_data = {
                'commerce': None,
                'category': None,
                'commerce_logo': None,
            }

            if keyword:
                commerce = keyword.merchant
                category = commerce.category if commerce else None

                if category:
                    categorized_transactions += 1

                if commerce:
                    identified_commerce_transactions += 1

                enriched_data.update({
                    'commerce': commerce.merchant_name if commerce else None,
                    'category': category.name if category else None,
                    'commerce_logo': commerce.merchant_logo if commerce else None,
                })

                # Check if the category type matches the expected type (case-insensitive)
                expected_category_type = self.get_expected_category_type(amount).lower()
                actual_category_type = category.type.lower() if category else None

                if category and actual_category_type != expected_category_type:
                    raise ValueError(f"The category type ({actual_category_type}) does not match the expected type for the transaction.")

            enriched_transaction = {
                'id': transaction['id'],
                'description': description,
                'amount': amount,
                'date': date,
                'enriched_data': enriched_data,
            }

            enriched_transactions.append(enriched_transaction)

        # Calculate metrics
        total_transactions = len(transactions)
        categorization_rate = categorized_transactions / total_transactions if total_transactions > 0 else 0
        commerce_identification_rate = identified_commerce_transactions / total_transactions if total_transactions > 0 else 0

        enrichment_detail = {
            'total_transactions': total_transactions,
            'categorization_rate': categorization_rate,
            'commerce_identification_rate': commerce_identification_rate,
        }

        return {'enriched_transactions': enriched_transactions, 'enrichment_detail': enrichment_detail}

    def get_expected_category_type(self, amount):
        # Determine the expected category type based on the sign of the amount
        return 'expense' if amount < 0 else 'income'
