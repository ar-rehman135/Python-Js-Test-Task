
from rest_framework import serializers
from product_search.models import Product ,SelectedProduct

class ProductSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock']

class SelectedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedProduct
        fields = ['id', 'user', 'product']
        read_only_fields = ['user']  
