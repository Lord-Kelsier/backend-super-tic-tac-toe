from rest_framework import serializers
from .models import Lobby
from authentication.serializers import UserSerializer
from superttt.serializers import GameSeralizer

class LobbySerializer(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.username')
  started = serializers.ReadOnlyField()
  players = UserSerializer(many=True, read_only=True)
  game = GameSeralizer(read_only=True)
  
  class Meta:
    model = Lobby
    fields = '__all__'