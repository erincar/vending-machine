from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import serializers

from .exceptions import UsernameAlreadyExists
from .models import Product, VendingMachineUser


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    password = serializers.CharField(source="user.password", write_only=True)

    class Meta:
        model = VendingMachineUser
        fields = ["id", "username", "password", "deposit", "role"]
        read_only_fields = ["id", "username", "deposit", "role"]

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data["user"]["username"],
                password=validated_data["user"]["password"],
            )
            VendingMachineUser.objects.create(
                **{
                    **validated_data,
                    "user": user,
                },
            )
            return VendingMachineUser.objects.get(user=user)
        except IntegrityError as e:
            if "UNIQUE constraint" in str(e.args):
                raise UsernameAlreadyExists()


class ProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(
        source="seller.user.username",
        read_only=True,
    )

    class Meta:
        model = Product
        fields = ["id", "seller_name", "name", "price", "quantity"]
        read_only_fields = ["id", "seller_name"]

    def create(self, validated_data):
        user = VendingMachineUser.objects.get(
            user=self.context["request"].user
        )
        return Product.objects.create(
            seller=user,
            **validated_data,
        )
