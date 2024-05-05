from rest_framework import serializers
from .models import SuperTTT, SuperTTTPlayer, Game

class SuperTTTPlayerSerializer(serializers.ModelSerializer):
  class Meta:
    model = SuperTTTPlayer
    fields = '__all__'

class SuperTTTSerializer(serializers.ModelSerializer):
  players = SuperTTTPlayerSerializer(many=True, read_only=True)
  class Meta:
    model = SuperTTT
    fields = '__all__'

class GameSeralizer(serializers.ModelSerializer):
  class Meta:
    model = Game
    fields = '__all__'