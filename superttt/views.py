from .models import SuperTTT
from .serializers import SuperTTTSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class SuperTTTViews(viewsets.ViewSet):
  serializer_class = SuperTTTSerializer
  queryset = SuperTTT.objects.all()
  def retrieve(self, request, pk=None):
    game = get_object_or_404(self.queryset, pk=pk)
    game_serialized = SuperTTTSerializer(game) 
    return Response(data=game_serialized.data, status=status.HTTP_200_OK)

  def partial_update(self, request, pk=None):
    pass
