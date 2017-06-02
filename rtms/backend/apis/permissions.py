# -*- coding: utf-8 -*-

from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication


class PlanExecutePermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.group in request.user.groups.all()

    # def has_permission(self, request, view):
    #     print 22222222222222
    #     # print view.get_queryset()
    #     # print dir(view)
    #     # print view.get_object()
    #     return True


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
