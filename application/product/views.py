import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
import csv
import os
from .models import Product
from django.db.models import Sum
from .service import clean_data

def load_data_view(request):
    """Load data from CSV and insert into the Product table."""
    csv_file_path = os.path.join(os.path.dirname(__file__), 'Test_Data.csv')

    data = pd.read_csv(csv_file_path)
    data = clean_data(data)
    products = [
        Product(
            product_id=row['product_id'],
            product_name=row['product_name'],
            category=row['category'],
            price=row['price'],
            quantity_sold=row['quantity_sold'],
            rating=row['rating'],
            review_count=row['review_count']
        )
        for _, row in data.iterrows()
    ]
    Product.objects.bulk_create(products, ignore_conflicts=True)
    return HttpResponse("Data uploaded successfully")

def generate_summary_report(request):
    """Generate a summary report and return as CSV."""
    categories = Product.objects.values('category').distinct()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="summary_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Category', 'Total Revenue', 'Top Product', 'Top Product Quantity Sold'])

    for category in categories:
        category_name = category['category']
        total_revenue = Product.objects.filter(category=category_name).aggregate(total_revenue=Sum('price'))['total_revenue']
        top_product = Product.objects.filter(category=category_name).order_by('-quantity_sold').first()
        writer.writerow([category_name, total_revenue, top_product.product_name, top_product.quantity_sold])

    return response
