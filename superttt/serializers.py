from rest_framework import serializers
from .models import SuperTTT

class SuperTTTSerializer(serializers.ModelSerializer):
  class Meta:
    model = SuperTTT
    fields = '__all__'