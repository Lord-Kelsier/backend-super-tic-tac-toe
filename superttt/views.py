from .models import SuperTTT, SuperTTTPlayer
from .serializers import SuperTTTSerializer
from rest_framework import viewsets, status, schemas
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from lobbies.permissions import IsInsideLobby
from .permissions import IsInTurn
import coreapi
import coreschema

make_move_schema = schemas.ManualSchema(
    fields=[
        coreapi.Field(
            "outer_board_id",
            location="query",
            required=True,
            schema=coreschema.Integer(
                title="outer_board_id",
                description="index of outer board",
            )
        ),
        coreapi.Field(
            "inner_board_id",
            location="query",
            required=True,
            schema=coreschema.Integer(
                title="inner_board_id",
                description="index of the inner board",
            )
        ),
    ],
    description="It enables you to enter or leave a lobby. In case, you are the owner of the lobby, it gets deleted upon leave.",
)

class SuperTTTViews(viewsets.ViewSet):
  serializer_class = SuperTTTSerializer
  queryset = SuperTTT.objects.all()
  permission_classes = [IsInsideLobby]
  def retrieve(self, request, pk=None):
    game = get_object_or_404(self.queryset, pk=pk)
    game_serialized = SuperTTTSerializer(game) 
    body = {
      "gameData": game_serialized.data,
      "isUserInside": request.user in game.lobby.players.all()
    }
    return Response(data=body, status=status.HTTP_200_OK)

  @action(detail=True, methods=['patch'], schema=make_move_schema, permission_classes=[IsInTurn])
  def make_move(self, request, pk=None):
    game = get_object_or_404(self.queryset, pk=pk)
    self.check_object_permissions(request, game)

    outer_board_id = request.data['outer_board_id']
    inner_board_id = request.data['inner_board_id']

    if not 0 <= outer_board_id < 9:
      return Response(data={
        'detail': 'invalid range of outer board id'
      }, status=status.HTTP_400_BAD_REQUEST)
    
    if not 0 <=inner_board_id < 9:
      return Response(data={
        'detail': 'invalid range of inner board id'
      }, status=status.HTTP_400_BAD_REQUEST)
    
    player = SuperTTTPlayer.objects.get(user=request.user)
    valid, new_game_state = game.make_move(outer_board_id, inner_board_id, player)
    if not valid:
      return Response({
        'data': 'move is not valid'
      }, status=status.HTTP_400_BAD_REQUEST)
    new_game_serialized = SuperTTTSerializer(new_game_state)
    return Response(new_game_serialized.data, status=status.HTTP_200_OK)
    
