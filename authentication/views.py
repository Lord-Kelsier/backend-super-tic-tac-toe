from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer
from rest_framework import viewsets, permissions, generics

class UserViewSet(viewsets.ModelViewSet):
  serializer_class = UserSerializer
  queryset = User.objects.all()


class RegisterView(generics.CreateAPIView):
  queryset = User.objects.all()
  permission_classes = [permissions.AllowAny]
  serializer_class = RegisterSerializer