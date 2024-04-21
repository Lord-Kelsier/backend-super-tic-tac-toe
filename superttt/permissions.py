from rest_framework import permissions

class IsInTurn(permissions.BasePermission):
  """
  Custom permission to only allow players in turn to make a move.
  """

  def has_object_permission(self, request, view, obj):
    return False
    user  = request.user
    player = obj.players.filter(user = user.id)
    print("player selected", player, flush=True)
    return obj.turn == player.symbol