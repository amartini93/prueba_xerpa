import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from data_enrichment.models import Transaction, Category, Commerce, Keyword

class Command(BaseCommand):
    """
    Load data from Excel file into the database
    """

    def handle(self, *args, **options):
        # Get the directory path where the script is located
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Navigate up four levels to the directory containing the Excel file
        file_path = os.path.abspath(os.path.join(script_directory, '..', '..', '..', '..', 'data/Prueba técnica - Backend Data .xlsx'))

        # Read data from Excel file into Pandas DataFrames for each sheet
        df_transaction = pd.read_excel(file_path, sheet_name='Transacciones')
        df_category = pd.read_excel(file_path, sheet_name='Categorías')
        df_commerce = pd.read_excel(file_path, sheet_name='Comercios')
        df_keywords = pd.read_excel(file_path, sheet_name='Keywords')

        # Load data for Transaction entity
        for _, row in df_transaction.iterrows():
            amount = row['amount']
            amount = None if pd.isna(amount) else amount

            date_str = row['date']
            date_value = None if pd.isna(date_str) else parse_date(date_str)

            transaction, created = Transaction.objects.get_or_create(
                id=row['id'],
                defaults={
                    'description': row['description'],
                    'amount': amount,
                    'date': date_value,
                }
            )

        # Load data for Category entity
        for _, row in df_category.iterrows():
            category, created = Category.objects.get_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'type': row['type'],
                }
            )

        # Load data for Commerce entity
        for _, row in df_commerce.iterrows():
            commerce, created = Commerce.objects.get_or_create(
                id=row['id'],
                defaults={
                    'merchant_name': row['merchant_name'],
                    'merchant_logo': row['merchant_logo'],
                }
            )

            # Retrieve the Category instance and assign it
            if not pd.isna(row['category_id']):
                category_instance, _ = Category.objects.get_or_create(id=row['category_id'])
                commerce.category = category_instance

            if not created:
                # If the object already exists, update its attributes
                commerce.merchant_name = row['merchant_name']
                commerce.merchant_logo = row['merchant_logo']

            commerce.save()

        # Load data for Keywords entity
        for _, row in df_keywords.iterrows():
            keyword, created = Keyword.objects.get_or_create(
                id=row['id'],
                defaults={
                    'keyword': row['keyword'],
                }
            )

            # Retrieve the Commerce instance and assign it
            if not pd.isna(row['merchant_id']):
                commerce_instance, _ = Commerce.objects.get_or_create(id=row['merchant_id'])
                keyword.merchant = commerce_instance  # Assuming merchant is the ForeignKey field

            if not created:
                # If the object already exists, update its attributes
                keyword.keyword = row['keyword']

            keyword.save()

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
