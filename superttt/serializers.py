from rest_framework import serializers
from .models import SuperTTT, SuperTTTPlayer

class SuperTTTPlayerSerializer(serializers.ModelSerializer):
  class Meta:
    model = SuperTTTPlayer
    fields = '__all__'

class SuperTTTSerializer(serializers.ModelSerializer):
  players = SuperTTTPlayerSerializer(many=True, read_only=True)
  class Meta:
    model = SuperTTT
    fields = '__all__'