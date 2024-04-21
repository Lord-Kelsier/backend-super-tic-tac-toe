from rest_framework.test import APITestCase
from .models import SuperTTT, GameType, SuperTTTPlayerSymbol
from lobbies.tests import create_lobby, create_user
from django.urls import reverse

def create_game(gameType=GameType.SUPERTTT):
  if gameType == GameType.SUPERTTT:
    return SuperTTT.objects.create(
      gameType = GameType.SUPERTTT.value,
      lobby = create_lobby(),
      turn = SuperTTTPlayerSymbol.CIRCLE,
      board = [[SuperTTTPlayerSymbol.NONE.value for _ in range(10)] for __ in range(9)]
    )
class SuperTTTModelStartGameTest(APITestCase):
  def test_start_game(self):
    lobby = create_lobby()
    newUser = create_user()
    lobby.add_player(newUser)
    self.client.force_authenticate(user = lobby.owner)
    response = self.client.get(reverse('lobby-detail', args=[lobby.id]))
    self.assertEqual(response.status_code, 200)
    response = self.client.patch(reverse('lobby-start-game'), data={"lobby_id": lobby.id})
    self.assertEqual(response.status_code, 202)
    game = response.data['game']
    response = self.client.get(reverse('game-detail', args=[game['id']]))
    self.assertEqual(response.status_code, 200)
    expected_board = [[0 for _ in range(10)] for __ in range(9)]
    self.assertListEqual(response.data['board'], expected_board)
  
  def test_permissions(self):
    pass

  def test_make_moves(self):
    lobby = create_lobby()
    newUser = create_user()
    lobby.add_player(newUser)
    self.client.force_authenticate(user = lobby.owner)
    response = self.client.patch(reverse('lobby-start-game'), data={"lobby_id": lobby.id})
    response = self.client.patch(
      reverse('game-make-move', args=[response.data['game']['id']]),
      data={
        'outer_board_id': 0,
        'inner_board_id': 0
      }
    )
    self.assertTrue(response.data['isValid'])
    expected_board = [[0 for _ in range(10)] for __ in range(9)]
    expected_board[0][0] = 1
    self.assertEqual(response.data['game']['board'], expected_board)
  