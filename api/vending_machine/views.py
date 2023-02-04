from rest_framework import decorators, permissions, status, viewsets
from rest_framework.response import Response

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


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.IsAuthenticated])
def deposit(request):
    if "coin" not in request.data or len(request.data.keys()) != 1:
        return Response(
            {"message": "An object with only the 'coin' field is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    accepted_coins = {5, 10, 20, 50, 100}
    if request.data["coin"] not in accepted_coins:
        return Response(
            {"message": f"Coin value should be one of {accepted_coins}."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    machine_user = VendingMachineUser.objects.get(user=request.user)
    machine_user.deposit += request.data["coin"]
    machine_user.save(update_fields=["deposit"])
    return Response({"deposit": machine_user.deposit})


@decorators.api_view(["PUT"])
@decorators.permission_classes([permissions.IsAuthenticated])
def reset(request):
    machine_user = VendingMachineUser.objects.get(user=request.user)
    machine_user.deposit = 0
    machine_user.save(update_fields=["deposit"])
    return Response(
        {"deposit": machine_user.deposit},
        status=status.HTTP_202_ACCEPTED,
    )


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.IsAuthenticated])
def buy(request):
    if "product_id" not in request.data or len(request.data.keys()) != 1:
        return Response(
            {
                "message": (
                    "An object with only the 'product_id' field is required."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        machine_user = VendingMachineUser.objects.get(user=request.user)
        product = Product.objects.get(id=request.data["product_id"])
        if machine_user.deposit < product.price:
            return Response(
                {"message": "Insufficient funds, please deposit coins."},
                status=status.HTTP_402_PAYMENT_REQUIRED,
            )
        if product.quantity < 1:
            return Response(
                {"message": "The product is not in stock."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        machine_user.deposit -= product.price
        product.quantity -= 1
        machine_user.save(update_fields=["deposit"])
        product.save(update_fields=["quantity"])
        return Response(status=status.HTTP_202_ACCEPTED)
    except Product.DoesNotExist:
        return Response(
            {"message": "The specified product was not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
