from rest_framework import permissions, viewsets

from .models import Product, VendingMachineUser
from .permissions import IsOwner, IsOwnUser
from .serializers import ProductSerializer, UserSerializer


class UserView(viewsets.ModelViewSet):
    queryset = VendingMachineUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        match self.action:
            case "list":
                self.permission_classes = [permissions.IsAdminUser]
            case "create":
                self.permission_classes = []
            case "retrieve":
                self.permission_classes = [permissions.IsAuthenticated]
            case "update" | "partial_update" | "destroy":
                self.permission_classes = [
                    permissions.IsAuthenticated,
                    IsOwnUser,
                ]
        return super().get_permissions()


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        match self.action:
            case "list" | "create" | "retrieve":
                self.permission_classes = [permissions.IsAuthenticated]
            case "update" | "partial_update" | "destroy":
                self.permission_classes = [
                    permissions.IsAuthenticated,
                    IsOwner,
                ]
        return super().get_permissions()

