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
  turn = models.IntegerField(choices=SuperTTTPlayerSymbol)
  board = ArrayField(
    ArrayField(
      models.IntegerField(choices=SuperTTTPlayerSymbol),
      size=10
    ),
    size=9
  )
  winner = models.IntegerField(SuperTTTPlayerSymbol, default=SuperTTTPlayerSymbol.NONE)
  canMoveAnywhere = models.BooleanField(default=True)
  nextBoardIndex = models.SmallIntegerField(default=0)

  def set_next_constraints(self, inner_board_id):
    if self.board[inner_board_id][9] != SuperTTTPlayerSymbol.NONE:
      self.canMoveAnywhere = True
    else:
      self.canMoveAnywhere = False
      self.nextBoardIndex = inner_board_id

  def make_move(self, outer_board_id, inner_board_id, player):
    valid = True
    if self.board[outer_board_id][inner_board_id] != SuperTTTPlayerSymbol.NONE:
      return not valid, self
    if self.board[outer_board_id][9] != SuperTTTPlayerSymbol.NONE:
      return not valid, self
    if not self.canMoveAnywhere and self.nextBoardIndex != outer_board_id:
      return not valid, self
    self.board[outer_board_id][inner_board_id] = player.symbol
    board_ended, board_winner = self.check_innner_board_win(board_index=outer_board_id)
    self.turn = SuperTTTPlayerSymbol.CROSS if self.turn == SuperTTTPlayerSymbol.CIRCLE else SuperTTTPlayerSymbol.CIRCLE
    self.set_next_constraints(inner_board_id)
    self.save()
    if not board_ended:
      return valid, self
    self.board[outer_board_id][9] = board_winner
    self.save()
    game_ended, winner = self.check_winner()
    if not game_ended:
      return valid, self
    self.turn = SuperTTTPlayerSymbol.NULLPLAYER
    self.winner = winner
    self.ended = True
    self.save()
    return valid, self
  
  def check_winner(self):
    board = self.board
    player_symbols = {SuperTTTPlayerSymbol.CIRCLE, SuperTTTPlayerSymbol.CROSS}
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
      if board[i][9] == SuperTTTPlayerSymbol.NONE:
        return False, SuperTTTPlayerSymbol.NONE
    # Draw
    return True, SuperTTTPlayerSymbol.NULLPLAYER
     
      
      

  def check_innner_board_win(self, board_index) -> Tuple[bool, SuperTTTPlayerSymbol]:
    inner_board = self.board[board_index]
    # Check rows
    for i in range(0, 9, 3):
      if inner_board[i] == inner_board[i + 1] == inner_board[i + 2] and inner_board[i] != SuperTTTPlayerSymbol.NONE:
        return True, inner_board[i]
    # Check columns
    for i in range(3):
      if inner_board[i] == inner_board[i + 3] == inner_board[i + 6] and inner_board[i] != SuperTTTPlayerSymbol.NONE:
        return True, inner_board[i]
    # Check diagonals
    if inner_board[0] == inner_board[4] == inner_board[8] and inner_board[i] != SuperTTTPlayerSymbol.NONE:
      return True, inner_board[0]
    if inner_board[2] == inner_board[4] == inner_board[6] and inner_board[i] != SuperTTTPlayerSymbol.NONE:
      return True, inner_board[2]
    # Check if filled
    for i in range(9):
      if inner_board[i] == SuperTTTPlayerSymbol.NONE:
        return False, SuperTTTPlayerSymbol.NONE
    # In case of draw
    return True, SuperTTTPlayerSymbol.NULLPLAYER


  def get_default_game(lobby, circle, cross):
    game = SuperTTT.objects.create(
      gameType = lobby.gameType,
      lobby = lobby,
      turn = SuperTTTPlayerSymbol.CIRCLE,
      board = [[SuperTTTPlayerSymbol.NONE for _ in range(10)] for __ in range(9)]
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
    text = f"ID: {self.id} Turn: {self.turn} HasEnded: {self.ended} board: {self.board}\n"
    text += f"gameType: {self.gameType}\n"
    text += f"Lobby: {self.lobby}\n"
    text += f"Winner: {self.winner}"
    return text

class SuperTTTPlayer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  symbol = models.IntegerField(choices=SuperTTTPlayerSymbol)
  game = models.ForeignKey(SuperTTT, on_delete=models.CASCADE, related_name='players')