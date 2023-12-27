from django.contrib import admin
from .models import Category, Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'amount', 'date')
    search_fields = ('id',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    search_fields = ('id','type')
