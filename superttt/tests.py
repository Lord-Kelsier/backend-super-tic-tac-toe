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
      board = [[SuperTTTPlayerSymbol.NONE for _ in range(10)] for __ in range(9)]
    )
class SuperTTTModelInteractionTest(APITestCase):
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
      reverse('game-make-move', args=[response.data['id']]),
      data={
        'outer_board_id': 0,
        'inner_board_id': 0
      }
    )
    self.assertEqual(response.status_code, 200)
    expected_board = [[0 for _ in range(10)] for __ in range(9)]
    expected_board[0][0] = 1
    self.assertEqual(response.data['board'], expected_board)

def make_move(client, game_id, outer, inner, player):
  client.force_authenticate(user = player)
  response = client.patch(
    reverse('game-make-move', args=[game_id]),
    data={
      'outer_board_id': outer,
      'inner_board_id': inner
    }
  )
  return response

class SuperTTTGameTest(APITestCase):
  def test_happy_path(self):
    lobby = create_lobby()
    player1 = lobby.owner
    player2 = create_user()
    lobby.add_player(player2)
    self.client.force_authenticate(user = player1)
    response = self.client.patch(reverse('lobby-start-game'), data={"lobby_id": lobby.id})
    game_id = response.data['id']
    response = make_move(self.client, game_id, 0, 0, player1)
    response = make_move(self.client, game_id, 0, 4, player2)
    response = make_move(self.client, game_id, 4, 0, player1)
    response = make_move(self.client, game_id, 0, 1, player2)
    response = make_move(self.client, game_id, 1, 0, player1)
    response = make_move(self.client, game_id, 0, 7, player2)

    expected_board = [
      [1, 2, 0, 0, 2, 0, 0, 2, 0, 2],
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    self.assertListEqual(response.data['board'], expected_board)
    self.assertFalse(response.data['ended'])
    self.assertEqual(response.data['winner'], 0)
    response = make_move(self.client, game_id, 7, 4, player1)
    response = make_move(self.client, game_id, 4, 4, player2)
    response = make_move(self.client, game_id, 4, 8, player1)
    response = make_move(self.client, game_id, 8, 8, player2)
    response = make_move(self.client, game_id, 8, 4, player1)
    response = make_move(self.client, game_id, 4, 3, player2)
    response = make_move(self.client, game_id, 3, 4, player1)
    response = make_move(self.client, game_id, 4, 5, player2)

    expected_board = [
      [1, 2, 0, 0, 2, 0, 0, 2, 0, 2],
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
      [1, 0, 0, 2, 2, 2, 0, 0, 1, 2],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0, 2, 0],
    ]
    self.assertListEqual(response.data['board'], expected_board)
    self.assertFalse(response.data['ended'])
    self.assertEqual(response.data['winner'], 0)
    response = make_move(self.client, game_id, 5, 8, player1)
    response = make_move(self.client, game_id, 8, 2, player2)
    response = make_move(self.client, game_id, 2, 8, player1)
    response = make_move(self.client, game_id, 8, 5, player2)
    
    expected_board = [
      [1, 2, 0, 0, 2, 0, 0, 2, 0, 2],
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
      [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
      [1, 0, 0, 2, 2, 2, 0, 0, 1, 2],
      [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 2, 0, 1, 2, 0, 0, 2, 2],
    ]
    self.assertListEqual(response.data['board'], expected_board)
    self.assertTrue(response.data['ended'])
    self.assertEqual(response.data['winner'], 2)