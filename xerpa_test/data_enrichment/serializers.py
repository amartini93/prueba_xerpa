from rest_framework import serializers
from .models import Transaction, Category, Commerce, Keyword

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommerceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commerce
        fields = '__all__'

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'
