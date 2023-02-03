from rest_framework import permissions


class IsOwnUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == "seller" and obj.seller.id == request.user.id
        )
