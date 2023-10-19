from django.views import View
from rest_framework import permissions
from rest_framework.request import Request


class DeleteStaffOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        if request.method == "DELETE":
            return request.user.is_staff
