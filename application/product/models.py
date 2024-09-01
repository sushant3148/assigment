from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=100, primary_key=True)
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_sold = models.IntegerField()
    rating = models.FloatField()
    review_count = models.IntegerField()

    def __str__(self):
        return self.product_name
