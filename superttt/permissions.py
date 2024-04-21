from rest_framework import permissions

class IsInTurn(permissions.BasePermission):
  """
  Custom permission to only allow players in turn to make a move.
  """

  def has_object_permission(self, request, view, obj):
    user  = request.user
    player = obj.players.filter(user = user.id)[0]
    return obj.turn == player.symbol