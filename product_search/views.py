from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import Product
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from .pagination import StandardResultsPagination
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404



# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSearchSerializer
    pagination_class = StandardResultsPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'search', openapi.IN_QUERY, description="Search products by name",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'sort', openapi.IN_QUERY, description="Sort products by a field (id, name, price, stock, description). Prefix with '-' for descending order.",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    @action(detail=True, methods=['get'])
    def list(self, request, *args, **kwargs):
        try:
            # Get the search query and sort parameters if present
            search_query = request.query_params.get('search', '')
            sort_query = request.query_params.get('sort', 'id')  # Default sort by 'id'
            
            # Determine the sorting direction
            if sort_query.startswith('-'):
                sort_field = sort_query[1:]
                sort_order = '-'
            else:
                sort_field = sort_query
                sort_order = ''
            
            # Ensure the sort field is valid
            valid_sort_fields = ['id', 'name', 'price', 'stock','description']
            if sort_field not in valid_sort_fields:
                sort_field = 'id'  # Default fallback if invalid sort field is given

            # Filter products based on the search query
            products = Product.objects.all()
            if search_query:
                products = products.filter(name__icontains=search_query)
            
            # Apply sorting
            products = products.order_by(f"{sort_order}{sort_field}")

            # Paginate the queryset
            paginated_products = self.paginate_queryset(products)
            if paginated_products is not None:
                serializer = self.get_serializer(paginated_products, many=True)
                return self.get_paginated_response(serializer.data)

            # If pagination is not applied, return the full result
            serializer = self.get_serializer(products, many=True)
            return Response({
                "status": "success",
                "message": "Products retrieved successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                "status": "error",
                "message": "An error occurred while retrieving products.",
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    @action(detail=True, methods=['post'])
    def create(self, request, *args, **kwargs):
        try:
            
            serializer = self.get_serializer(data=request.data)
            
            # Validate data and raise exception if invalid
            serializer.is_valid(raise_exception=True)
            product = serializer.save()
            
            # Success response
            return Response({
                "status": "success",
                "message": "Product created successfully.",
                "data": {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "stock": product.stock,
                }
            }, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            # If validation error, return detailed field errors
            return Response({
                "status": "error",
                "message": "Validation failed.",
                "errors": e.detail  # Detailed validation errors by field
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # For any other unforeseen errors, return a generic error message
            return Response({
                "status": "error",
                "message": "An unexpected error occurred while creating the product.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        responses={
            200: "Product marked as selected.",
            404: "Product not found.",
            500: "An error occurred."
        }
    )
    def select_product(self, request, pk=None):
        try:
            product = self.get_object()
            product.selected = True
            product.save()
            return Response({
                "status": "success",
                "message": "Product marked as selected.",
                "data": {
                    "id": product.id,
                    "name": product.name,
                    "selected": product.selected
                }
            }, status=status.HTTP_200_OK)
        
        except Product.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Product not found.",
                "data": {}
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({
                "status": "error",
                "message": "An error occurred while marking the product as selected.",
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SelectedProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SelectedProduct.objects.all()
    serializer_class = SelectedProductSerializer
    pagination_class = StandardResultsPagination
    
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description="List of product IDs to select"
                )
            },
            required=['product_ids'],
            example={
                "product_ids": [1, 2, 3]
            }
        )
    )
    @action(detail=False, methods=['post'])
    def select_products(self, request):
        product_ids = request.data.get('product_ids', [])
        
        if not product_ids:
            return Response({
                "status": "error",
                "message": "No products selected."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Filter products by IDs and ensure only unique selections
        selected_products = []
        for product_id in product_ids:
            product = get_object_or_404(Product, id=product_id)
            selected_product, created = SelectedProduct.objects.get_or_create(user=request.user, product=product)
            if created:
                selected_products.append(selected_product)
        
        # Retrieve detailed information about each selected product
        selected_product_instances = Product.objects.filter(id__in=product_ids)
        product_serializer = ProductSearchSerializer(selected_product_instances, many=True)
        
        return Response({
            "status": "success",
            "message": "Products selected successfully.",
            "data": product_serializer.data  # Return full product details
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def selected_products(self, request):
        # Retrieve all products selected by the user
        selected_products = Product.objects.filter(selected_by_users__user=request.user)
        
        # Apply pagination
        page = self.paginate_queryset(selected_products)
        if page is not None:
            serializer = ProductSearchSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        # If pagination is not applied, return the full result
        serializer = ProductSearchSerializer(selected_products, many=True)
        
        return Response({
            "status": "success",
            "message": "Selected products retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)