from django.db import models
from django.contrib.auth.models import User

class Lobby(models.Model):

  class GameType(models.IntegerChoices):
    SUPERTTT = 0

  owner = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name='ownedLobby',
  )
  game = models.IntegerField(choices=GameType)
  title = models.CharField(max_length=255)
  started = models.BooleanField(default=False)
  players = models.ManyToManyField(User)
  def __str__(self) -> str:
    text = f"{self.title}:{"" if self.started else "not"} started | "
    text += f"owned by: {self.owner}|players:{list(map(lambda p: p.username ,self.players.all()))}"
    return text
