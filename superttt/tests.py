from rest_framework.test import APITestCase
from .models import SuperTTT, GameType, SuperTTTPlayerSymbol
from lobbies.tests import create_lobby

def create_game(gameType=GameType.SUPERTTT):
  if gameType == GameType.SUPERTTT:
    return SuperTTT.objects.create(
      gameType = GameType.SUPERTTT.value,
      lobby = create_lobby(),
      turn = SuperTTTPlayerSymbol.CIRCLE,
      board = [[SuperTTTPlayerSymbol.NONE.value for _ in range(10)] for __ in range(9)]
    )