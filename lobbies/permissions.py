from rest_framework import permissions
from lobbies.models import Lobby


class IsOwnerOrReadOnly(permissions.BasePermission):
  """
  Custom permission to only allow owners of an object to edit it.
  """

  def has_object_permission(self, request, view, obj):
    # Read permissions are allowed to any request,
    # so we'll always allow GET, HEAD or OPTIONS requests.
    if request.method in permissions.SAFE_METHODS:
      return True

    # Write permissions are only allowed to the owner of the snippet.
    return obj.owner == request.user

class IsInsideLobby(permissions.BasePermission):
  """
  Custom permission to only allow users inside a lobby to edit it
  """
  
  def has_object_permission(self, request, view, obj):
    user = request.user
    lobby = obj
    return lobby.players.contains(user)
  
class IsLobbyOwner(permissions.BasePermission):
  """
  Custom permission to only allow owners of an object to interact with it.
  """

  def has_object_permission(self, request, view, obj):
    return obj.owner == request.user
  
class IsNotInsideOtherLobby(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method != 'POST': return True
    user = request.user
    return not user.lobby.all().exists()