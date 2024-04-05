from rest_framework import permissions


class IsSelfOrReadOnly(permissions.BasePermission):
  """
  Custom permission to only allow owners of an object to edit it.
  """
  def has_permission(self, request, view):
    return request.method != 'POST'

  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    return obj == request.user