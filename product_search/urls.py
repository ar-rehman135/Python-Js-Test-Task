from django.urls import include, path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [ 
    
    # ProductViewSet endpoints 
    path('products/', ProductViewSet.as_view({'get': 'list'}), name='product-list'),
    path('product/create/', ProductViewSet.as_view({'post': 'create'}), name='product-create'),
    path('product/<int:pk>/select/', ProductViewSet.as_view({'get': 'select_product'}), name='product-list'),
     
    # SelectedProductViewSet endpoints
    path('product/select/', SelectedProductViewSet.as_view({'post': 'select_products'}), name='select_products'),
    path('product/selected/', SelectedProductViewSet.as_view({'get': 'selected_products'}), name='select_products'),
  
]