from django.core.management.base import BaseCommand
from product_search.models import Product  
import random

class Command(BaseCommand):
    help = "Insert dummy data into the Product table for testing."

    def handle(self, *args, **kwargs):
        # Define some dummy product data
        dummy_products = [
            {"name": "Laptop", "description": "A high-performance laptop", "price": 1200.99, "stock": 25},
            {"name": "Smartphone", "description": "Latest model smartphone", "price": 999.99, "stock": 50},
            {"name": "Headphones", "description": "Noise-cancelling headphones", "price": 199.99, "stock": 30},
            {"name": "Smartwatch", "description": "A smartwatch with multiple features", "price": 299.99, "stock": 40},
            {"name": "Tablet", "description": "A tablet for everyday use", "price": 499.99, "stock": 15},
            {"name": "Gaming Console", "description": "Next-gen gaming console", "price": 499.99, "stock": 20},
            {"name": "Monitor", "description": "4K Ultra HD monitor", "price": 299.99, "stock": 10},
            {"name": "Keyboard", "description": "Mechanical keyboard", "price": 89.99, "stock": 100},
            {"name": "Mouse", "description": "Wireless mouse", "price": 49.99, "stock": 200},
            {"name": "Charger", "description": "Fast charging USB-C charger", "price": 29.99, "stock": 150},
        ]

        # Insert dummy data into Product table
        for product_data in dummy_products:
            product, created = Product.objects.get_or_create(
                name=product_data["name"],
                defaults={
                    "description": product_data["description"],
                    "price": product_data["price"],
                    "stock": product_data["stock"],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Inserted product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product {product.name} already exists'))
        
        self.stdout.write(self.style.SUCCESS("Dummy products inserted successfully."))
