from rest_framework import viewsets, permissions, status, schemas
from rest_framework.decorators import action
from .serializer import LobbySerializer
from .models import Lobby
from .permissions import IsOwnerOrReadOnly, IsInsideLobby, IsLobbyOwner
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import coreapi
import coreschema

lobby_population_schema = schemas.ManualSchema(
    fields=[
        coreapi.Field(
            "lobby_id",
            location="query",
            required=True,
            schema=coreschema.Integer(
                title="lobby_id",
                description="ID of the lobby you want to enter/leave",
            )
        ),
    ],
    description="It enables you to enter or leave a lobby. In case, you are the owner of the lobby, it gets deleted upon leave.",
)
class LobbyView(viewsets.ModelViewSet):
  serializer_class = LobbySerializer
  queryset = Lobby.objects.all()
  permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
  
  def perform_create(self, serializer):
    serializer.save(owner=self.request.user, started=False, players=[self.request.user])
    
  @action(detail=False, methods=['patch'], permission_classes=[permissions.IsAuthenticated], schema=lobby_population_schema)
  def enter_lobby(self, request):
    pk = request.data['lobby_id']
    queryset = Lobby.objects.all()
    lobby = get_object_or_404(queryset, pk=pk)
    user = self.request.user
    print(user.lobby)
    if lobby.players.contains(user):
      return Response(data={
          'detail': f'Already inside lobby {lobby.title}'
        },
        status=status.HTTP_406_NOT_ACCEPTABLE
      )
    if lobby.players.count() >= 2:
      return Response(data={
          'detail': 'Lobby full, max 2 players'
        },
        status=status.HTTP_406_NOT_ACCEPTABLE
      )
    lobby.players.add(user)
    lobby.save()
    lobby_serializer = LobbySerializer(lobby)
    return Response(data=lobby_serializer.data, status=status.HTTP_202_ACCEPTED)
  
  @action(detail=False, methods=['patch'], permission_classes=[IsInsideLobby], schema=lobby_population_schema)
  def leave_lobby(self, request):
    pk = request.data['lobby_id']
    queryset = Lobby.objects.all()
    lobby = get_object_or_404(queryset, pk=pk)
    user = self.request.user
    if lobby.owner == user:
      lobby.delete()
      return Response(data={
          'detail': f'Lobby deleted, owner leave'
        },
        status=status.HTTP_202_ACCEPTED
      )
    
    lobby.players.remove(user)
    lobby.save()
    lobby_serializer = LobbySerializer(lobby)
    return Response(data=lobby_serializer.data, status=status.HTTP_202_ACCEPTED)
  
  @action(detail=False, methods=['patch'], permission_classes=[IsLobbyOwner], schema=lobby_population_schema)
  def start_game(self, request):
    pk = request.data['lobby_id']
    queryset = Lobby.objects.all()
    lobby = get_object_or_404(queryset, pk=pk)
    if lobby.players.count() != 2:
      return Response(data={
          'detail': 'Lobby must be full, 2 player needed for this game.'
        },
        status=status.HTTP_406_NOT_ACCEPTABLE
      )
    lobby.started = True
    lobby.save()
    lobby_serializer = LobbySerializer(lobby)
    # Falta lógica de inicio de juego
    return Response(data=lobby_serializer.data, status=status.HTTP_202_ACCEPTED)