from django.urls import include, path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [  
    path("auth/login/", LoginView.as_view({'post': 'login'}), name="login"),

  
]