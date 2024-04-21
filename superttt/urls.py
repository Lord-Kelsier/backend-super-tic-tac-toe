from django.urls import path, include
from rest_framework import routers
from .views import SuperTTTViews

router = routers.DefaultRouter()
router.register('', SuperTTTViews, basename='game')

urlpatterns = [
  path('', include(router.urls)),
]