from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import UserLoginSerializer
from auth_manager.models import CustomUser



class LoginView(viewsets.ModelViewSet):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
  
    def login(self, request, *args, **kwargs):
        try:
            # Validate input data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            
            # Retrieve user by email
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Invalid username or password. Please try again.",
                    "data": {}
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Check if user is active
            if not user.is_active:
                return Response({
                    "status": "error",
                    "message": "Your account has been disabled. Please contact support for assistance.",
                    "data": {}
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Check password
            if not user.check_password(password):
                return Response({
                    "status": "error",
                    "message": "Invalid username or password. Please try again.",
                    "data": {}
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Check if user is a superuser (if restricted)
            if user.is_superuser:
                return Response({
                    "status": "error",
                    "message": "Superusers are not allowed to login on this Portal!",
                    "data": {}
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Generate or retrieve token
            token, created = Token.objects.get_or_create(user=user)
            
            # Prepare response data
            response_data = {
                "token": token.key,
                "user_data": {
                    "id": user.id,
                    "email": user.email,
                }
            }

            return Response({
                "status": "success",
                "message": "Logged in successfully.",
                "data": response_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the exception if needed and provide a generic error message
            return Response({
                "status": "error",
                "message": "An error occurred during login. Please try again later.",
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





