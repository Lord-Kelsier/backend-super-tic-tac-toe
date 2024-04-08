from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from lobbies.models import Lobby
from .types import GameType, SuperTTTPlayerSymbol

class Game(models.Model):
  gameType = models.IntegerField(choices=GameType)
  ended = models.BooleanField(default=False)

class SuperTTT(Game):
  turn = models.IntegerField(SuperTTTPlayerSymbol)
  hasEnded = models.BooleanField(default=False)
  board = ArrayField(
    ArrayField(
      models.CharField(max_length=1, blank=False, default='-'),
      size=9
    ),
    size=9
  )

class SuperTTTPlayer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  symbol = models.IntegerField(choices=SuperTTTPlayerSymbol)
  hasWon = models.BooleanField(default=False)
  game = models.ForeignKey(SuperTTT, on_delete=models.CASCADE)