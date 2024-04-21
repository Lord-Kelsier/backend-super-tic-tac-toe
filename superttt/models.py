from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from .types import GameType, SuperTTTPlayerSymbol
from typing import Tuple

class Game(models.Model):
  gameType = models.IntegerField(choices=GameType)
  ended = models.BooleanField(default=False)
  lobby = models.OneToOneField('lobbies.Lobby', on_delete=models.CASCADE, related_name='game')

class SuperTTT(Game):
  turn = models.IntegerField(SuperTTTPlayerSymbol)
  board = ArrayField(
    ArrayField(
      models.IntegerField(choices=SuperTTTPlayerSymbol),
      size=10
    ),
    size=9
  )
  winner = models.IntegerField(SuperTTTPlayerSymbol, default=SuperTTTPlayerSymbol.NONE.value)
  def make_move(self, outer_board_id, inner_board_id, player):
    valid = True
    if self.board[outer_board_id][inner_board_id] != SuperTTTPlayerSymbol.NONE.value:
      return not valid, self
    if self.board[outer_board_id][9] != SuperTTTPlayerSymbol.NONE.value:
      return not valid, self
    self.board[outer_board_id][inner_board_id] = player.symbol
    board_ended, board_winner = self.check_innner_board_win(board_index=outer_board_id)
    self.turn = SuperTTTPlayerSymbol.CROSS.value if self.turn == SuperTTTPlayerSymbol.CIRCLE.value else SuperTTTPlayerSymbol.CIRCLE.value
    self.save()
    if not board_ended:
      return valid, self
    game_ended, winner = self.check_winner()
    if not game_ended:
      return valid, self
    self.turn = SuperTTTPlayerSymbol.NULLPLAYER.value
    self.winner = winner
    self.ended = True
    self.save()
    return valid, self
  
  def check_winner(self):
    board = self.board
    player_symbols = {SuperTTTPlayerSymbol.CIRCLE.value, SuperTTTPlayerSymbol.CROSS.value}
    # Check rows
    for i in range(0, 9, 3):
      if board[i][9] == board[i + 1][9] == board[i + 2][9] and board[i][9] in player_symbols:
        return True, board[i][9]
    # Check columns
    for i in range(3):
      if board[i][9] == board[i + 3][9] == board[i + 6][9] and board[i][9] in player_symbols:
        return True, board[i][9]
    # Check diagonals
    if board[0][9] == board[4][9] == board[8][9] and board[0][9] in player_symbols:
      return True, board[0][9]
    if board[2][9] == board[4][9] == board[6][9] and board[2][9] in player_symbols:
      return True, board[2][9]
    # Check if all filled
    for i in range(9):
      if board[i][9] == SuperTTTPlayerSymbol.NONE.value:
        return False, SuperTTTPlayerSymbol.NONE.value
    # Draw
    return True, SuperTTTPlayerSymbol.NULLPLAYER.value
     
      
      

  def check_innner_board_win(self, board_index) -> Tuple[bool, SuperTTTPlayerSymbol]:
    inner_board = self.board[board_index]
    # Check rows
    for i in range(0, 9, 3):
      if inner_board[i] == inner_board[i + 1] == inner_board[i + 2]:
        self.board[board_index][9] = inner_board[i]
        return True, inner_board[i]
    # Check columns
    for i in range(3):
      if inner_board[i] == inner_board[i + 3] == inner_board[i + 6]:
        self.board[board_index][9] = inner_board[i]
        return True, inner_board[i]
    # Check diagonals
    if inner_board[0] == inner_board[4] == inner_board[8]:
      self.board[board_index][9] = inner_board[0]
      return True, inner_board[0]
    if inner_board[2] == inner_board[4] == inner_board[6]:
      self.board[board_index][9] = inner_board[2]
      return True, inner_board[2]
    # Check if filled
    for i in range(9):
      if inner_board[i] == SuperTTTPlayerSymbol.NONE.value:
        return False, SuperTTTPlayerSymbol.NONE.value
    # In case of draw
    self.board[board_index][9] = SuperTTTPlayerSymbol.NULLPLAYER.value
    return True, SuperTTTPlayerSymbol.NULLPLAYER.value


  def get_default_game(lobby, circle, cross):
    game = SuperTTT.objects.create(
      gameType = lobby.gameType,
      lobby = lobby,
      turn = SuperTTTPlayerSymbol.CIRCLE.value,
      board = [[SuperTTTPlayerSymbol.NONE.value for _ in range(10)] for __ in range(9)]
    )
    circlePlayer = SuperTTTPlayer.objects.create(
      user = circle,
      symbol = SuperTTTPlayerSymbol.CIRCLE,
      game = game
    )
    crossPlayer = SuperTTTPlayer.objects.create(
      user = cross,
      symbol = SuperTTTPlayerSymbol.CROSS,
      game = game
    )
    game.players.set([circlePlayer, crossPlayer])
    return game
  
  def __str__(self) -> str:
    text = f"Turn: {self.turn} HasEnded: {self.ended} board: {self.board}\n"
    text += f"gameType: {self.gameType}\n"
    text += f"Lobby: {self.lobby}\n"
    text += f"Winner: {self.winner}"
    return text

class SuperTTTPlayer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  symbol = models.IntegerField(choices=SuperTTTPlayerSymbol)
  game = models.ForeignKey(SuperTTT, on_delete=models.CASCADE, related_name='players')