"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from authentication.views import UserViewSet, RegisterView
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('', UserViewSet, basename='user')

urlpatterns = [
  path('api-docs/', include_docs_urls('API')),
  path('admin/', admin.site.urls),
  path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('register/', RegisterView.as_view(), name='auth_register'),
  path('api/v1/lobby/', include('lobbies.urls')),
  path('api/v1/game/', include('superttt.urls')),
  path('api/v1/users/', include(router.urls))
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)