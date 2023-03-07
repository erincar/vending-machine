from rest_framework import permissions


class IsOwnUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.vendingmachineuser.role == "seller"
            and obj.seller.id == request.user.vendingmachineuser.id
        )


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.vendingmachineuser.role == "seller"
