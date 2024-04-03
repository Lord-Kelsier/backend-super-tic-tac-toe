from rest_framework.test import APITestCase
from .models import Lobby, User
from django.urls import reverse
from faker import Faker
from faker.providers import internet
from authentication.tests import create_user

def create_lobby(user: User = None, game = 0, title = None) -> Lobby:
  fake = Faker()
  fake.add_provider(internet)
  if not user:
    user = create_user()
  if not title:
    title = fake.domain_word()
  lobby = Lobby.objects.create(
    owner = user,
    game = game,
    title = title
  )
  lobby.players.set([user])
  user.lobby.add(lobby)
  return lobby

class LobbyViewDetailTest(APITestCase):
  def test_get_for_authentication(self):
    """
    GET /lobby/<id> allowed only to auth users
    """
    user = create_user()
    lobby = create_lobby(user)
    # not auth user
    request = self.client.get(reverse('lobby-detail', args=[lobby.id]))
    self.assertEqual(request.status_code, 401, 'Credentials needed to access')
    
    # auth user, but not owner
    other_user = create_user()
    self.client.force_authenticate(user = other_user)
    request = self.client.get(reverse('lobby-detail', args=[lobby.id]))
    self.assertEqual(request.status_code, 200, 'Auth users allowed')
    
    # auth owner user
    self.client.force_authenticate(user = user)
    request = self.client.get(reverse('lobby-detail', args=[lobby.id]))
    self.assertEqual(request.status_code, 200, 'Owner user allowed')
    
  def test_create_lobby(self):
    """
    POST is allowed only for auth users that are not inside other lobby
    """
    lobby = create_lobby()
    user_without_lobby = create_user()
    user_in_lobby = create_user()
    lobby.add_player(user_in_lobby)
    
    body = {
      "game": 0,
      "title": "myGame"
    }
    # No auth 
    request = self.client.post(reverse('lobby-list'),
      data = body
    )
    self.assertEqual(request.status_code, 401, 'Credentials needed for creating a lobby')
    
    # Owner of a lobby
    self.client.force_authenticate(user = lobby.owner)
    request = self.client.post(reverse('lobby-list'),
      data = body
    )
    self.assertEqual(request.status_code, 403, 'User owner of a lobby can\' create another lobby')
    
    # Player inside a lobby
    self.client.force_authenticate(user = user_in_lobby)
    request = self.client.post(reverse('lobby-list'),
      data = body
    )
    self.assertEqual(request.status_code, 403, 'User inside a lobby can\' create a lobby')
    
    # Player without lobby
    self.client.force_authenticate(user = user_without_lobby)
    request = self.client.post(reverse('lobby-list'),
      data = body
    )
    self.assertEqual(request.status_code, 201, 'User whithout lobby can create a lobby')
    
  def test_update_lobby(self):
    """
    PUT is allowed only for owners of a lobby
    """
    lobby = create_lobby()
    user_without_lobby = create_user()
    user_in_lobby = create_user()
    lobby.add_player(user_in_lobby)
    new_title = "myGame"
    body = {
      "game": 0,
      "title": new_title
    }
    url = reverse('lobby-detail', args=[lobby.id])
    # No auth 
    request = self.client.put(url,
      data = body
    )
    self.assertEqual(request.status_code, 401, 'Credentials needed for updating a lobby')
    
    # Player inside a lobby
    self.client.force_authenticate(user = user_in_lobby)
    request = self.client.put(url,
      data = body
    )
    self.assertEqual(request.status_code, 403, 'Only owners can modify the lobby')
    
    # Player without lobby
    self.client.force_authenticate(user = user_without_lobby)
    request = self.client.put(url,
      data = body
    )
    self.assertEqual(request.status_code, 403, 'Only owners can modify the lobby')
    
    # Owner of a lobby
    self.client.force_authenticate(user = lobby.owner)
    request = self.client.put(url,
      data = body
    )
    self.assertEqual(request.status_code, 200, 'User owner of a lobby can update the lobby')
    updated_lobby = Lobby.objects.get(id=lobby.id)
    self.assertEqual(updated_lobby.title, new_title)
    
  def test_partial_update_lobby(self):
    """
    PATCH is allowed only for owners of a lobby
    """
    lobby = create_lobby()
    user_without_lobby = create_user()
    user_in_lobby = create_user()
    lobby.add_player(user_in_lobby)
    new_title = "myGame"
    body = {
      "title": new_title
    }
    url = reverse('lobby-detail', args=[lobby.id])
    # No auth 
    request = self.client.patch(url,
      data = body
    )
    self.assertEqual(request.status_code, 401, 'Credentials needed for updating a lobby')
    
    # Player inside a lobby
    self.client.force_authenticate(user = user_in_lobby)
    request = self.client.patch(url,
      data = body
    )
    self.assertEqual(request.status_code, 403, 'Only owners can modify the lobby')
    
    # Player without lobby
    self.client.force_authenticate(user = user_without_lobby)
    request = self.client.patch(url,
      data = body
    )
    self.assertEqual(request.status_code, 403, 'Only owners can modify the lobby')
    
    # Owner of a lobby
    self.client.force_authenticate(user = lobby.owner)
    request = self.client.patch(url,
      data = body
    )
    self.assertEqual(request.status_code, 200, 'User owner of a lobby can update the lobby')
    updated_lobby = Lobby.objects.get(id=lobby.id)
    self.assertEqual(updated_lobby.title, new_title)
    
    
    
    
    
