from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from lobbies.models import Lobby
from .types import GameType, SuperTTTPlayerSymbol

class Game(models.Model):
  gameType = models.IntegerField(choices=GameType)
  ended = models.BooleanField(default=False)
  lobby = models.OneToOneField(Lobby, on_delete=models.CASCADE, related_name='game')

class SuperTTT(Game):
  turn = models.IntegerField(SuperTTTPlayerSymbol)
  board = ArrayField(
    ArrayField(
      models.CharField(max_length=1, blank=False),
      size=9
    ),
    size=9
  )

  def __str__(self) -> str:
    text = f"Turn: {self.turn} HasEnded: {self.ended} board: {self.board}\n"
    text += f"gameType: {self.gameType}\n"
    text += f"Lobby: {self.lobby}"
    return text

class SuperTTTPlayer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  symbol = models.IntegerField(choices=SuperTTTPlayerSymbol)
  hasWon = models.BooleanField(default=False)
  game = models.ForeignKey(SuperTTT, on_delete=models.CASCADE)