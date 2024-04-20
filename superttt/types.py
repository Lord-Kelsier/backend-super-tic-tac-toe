from django.db import models

class GameType(models.IntegerChoices):
  SUPERTTT = 0
  
class SuperTTTPlayerSymbol(models.IntegerChoices):
  NONE = 0
  CIRCLE = 1
  CROSS = 2