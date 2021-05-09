from rest_framework import permissions
from rest_framework.request import Request

from income.models import Income


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request: Request, view, obj: Income):
        return obj.owner == request.user
