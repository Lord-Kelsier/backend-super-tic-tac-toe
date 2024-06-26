from django.urls import path, include
from rest_framework import routers
from lobbies import views

router = routers.DefaultRouter()
router.register('', views.LobbyView, basename='lobby')

urlpatterns = [
  path('', include(router.urls)),
]