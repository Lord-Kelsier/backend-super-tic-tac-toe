from django.db import models

class GameType(models.IntegerChoices):
  SUPERTTT = 0
  
class SuperTTTPlayerSymbol(models.IntegerChoices):
  NONE = 0 # when none player has played
  CIRCLE = 1
  CROSS = 2
  NULLPLAYER = 3 # in case of draw, this is the winner of board