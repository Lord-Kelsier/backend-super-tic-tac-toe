from django.db import models

class GameType(models.IntegerChoices):
  SUPERTTT = 0
  
class SuperTTTPlayerSymbol(models.IntegerChoices):
  CIRCLE = 0
  CROSS = 1