from django.urls import include, path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [  
    path('products/', ProductViewSet.as_view({'get': 'list'}), name='product-list'),
    path('product/create/', ProductViewSet.as_view({'post': 'create'}), name='product-create'),
    path('product/<int:pk>/select/', ProductViewSet.as_view({'get': 'select_product'}), name='product-list'),
  
]