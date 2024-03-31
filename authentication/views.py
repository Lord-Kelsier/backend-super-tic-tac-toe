from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer
from rest_framework import viewsets, permissions, generics
from .permissions import IsSelfOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
  serializer_class = UserSerializer
  queryset = User.objects.all()
  permission_classes = [IsSelfOrReadOnly]


class RegisterView(generics.CreateAPIView):
  queryset = User.objects.all()
  permission_classes = [permissions.AllowAny]
  serializer_class = RegisterSerializer