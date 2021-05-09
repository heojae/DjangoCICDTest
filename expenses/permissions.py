from rest_framework import permissions
from rest_framework.request import Request

from expenses.models import Expense


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request: Request, view, obj: Expense):
        return obj.owner == request.user
