from django.db import models
from django.contrib.auth.models import User
from superttt.types import GameType
from superttt.models import SuperTTT

class Lobby(models.Model):
  owner = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name='ownedLobby',
  )
  gameType = models.IntegerField(GameType)
  title = models.CharField(max_length=255)
  started = models.BooleanField(default=False)
  players = models.ManyToManyField(User, related_name='lobby')
  
  def __str__(self) -> str:
    text = f"{self.title}:{"" if self.started else "not"} started | "
    text += f"owned by: {self.owner}|players:{list(map(lambda p: p.username ,self.players.all()))}"
    return text
  
  def add_player(self, player: User) -> None:
    # check if not inside
    self.players.add(player)
  
  def remove_player(self, player: User) -> None:
    # check if inside
    self.players.remove(player)

  def start_game(self) -> None:
    users = self.players.all()
    game = SuperTTT.get_default_game(lobby = self, circle = users[0], cross = users[1])
    self.game = game
    self.started = True
    self.save()