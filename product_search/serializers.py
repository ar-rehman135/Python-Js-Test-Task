
from rest_framework import serializers
from product_search.models import Product 

class ProductSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock','selected']
