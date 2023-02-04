from base64 import b64encode

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Product, VendingMachineUser

User = get_user_model()


def create_auth_header(username: str, password: str):
    auth = b64encode(f"{username}:{password}".encode()).decode()
    return f"Basic {auth}"


class UserViewTestCase(APITestCase):
    def setUp(self):
        self.password = "password"
        self.admin_user: User = User.objects.create_superuser(
            username="admin",
            password=self.password,
            email="admin@tests.com",
        )
        self.regular_user: User = User.objects.create_user(
            username="test_user",
            password=self.password,
        )

    def test_list_users_should_fail_for_non_admin(self):
        response = self.client.get(
            reverse("user-list"),
            HTTP_AUTHORIZATION=create_auth_header(
                self.regular_user.username, self.password
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_should_succeed_for_admin(self):
        response = self.client.get(
            reverse("user-list"),
            HTTP_AUTHORIZATION=create_auth_header(
                self.admin_user.username, self.password
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_create_user_with_correct_data_should_succeed(self):
        data = {"username": "new_user", "password": "newpassword"}
        response = self.client.post(reverse("user-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VendingMachineUser.objects.count(), 1)
        self.assertEqual(
            VendingMachineUser.objects.filter(
                user__username=data["username"]
            ).count(),
            1,
        )

    def test_update_other_user_should_fail_as_requesting_user(self):
        users = [
            User.objects.create_user(
                username=f"update_test_user{i}",
                password=self.password,
            )
            for i in range(2)
        ]
        requesting_user, other_user = [
            VendingMachineUser.objects.create(
                user=user,
            )
            for user in users
        ]
        response = self.client.patch(
            reverse("user-detail", kwargs={"pk": other_user.id}),
            {},
            format="json",
            HTTP_AUTHORIZATION=create_auth_header(
                requesting_user.user.username, self.password
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_own_user_should_succeed(self):
        machine_user = VendingMachineUser.objects.create(
            user=User.objects.create_user(
                username="update_own_user",
                password=self.password,
            ),
            role="buyer",
        )
        data = {"role": "seller"}
        response = self.client.patch(
            reverse("user-detail", kwargs={"pk": machine_user.id}),
            data,
            format="json",
            HTTP_AUTHORIZATION=create_auth_header(
                machine_user.user.username, self.password
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role"], data["role"])


class DepositViewTestCase(APITestCase):
    def setUp(self):
        self.password = "password"
        self.regular_user: User = User.objects.create_user(
            username="test_user",
            password=self.password,
        )
        self.machine_user = VendingMachineUser.objects.create(
            user=self.regular_user,
            role="buyer",
            deposit=0,
        )

    def test_deposit_should_succeed_with_valid_coin(self):
        previous_deposit = self.machine_user.deposit
        data = {"coin": 10}
        response = self.client.post(
            reverse("deposit"),
            data,
            format="json",
            HTTP_AUTHORIZATION=create_auth_header(
                self.regular_user.username, self.password
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["deposit"], previous_deposit + data["coin"]
        )

    def test_deposit_should_fail_with_negative_coin(self):
        self.machine_user.deposit
        data = {"coin": -5}
        response = self.client.post(
            reverse("deposit"),
            data,
            format="json",
            HTTP_AUTHORIZATION=create_auth_header(
                self.regular_user.username, self.password
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deposit_should_fail_with_non_existent_coin(self):
        self.machine_user.deposit
        data = {"coin": 7}
        response = self.client.post(
            reverse("deposit"),
            data,
            format="json",
            HTTP_AUTHORIZATION=create_auth_header(
                self.regular_user.username, self.password
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BuyViewTestCase(APITestCase):
    def setUp(self):
        self.password = "password"
        self.seller: User = VendingMachineUser.objects.create(
            user=User.objects.create_user(
                username="test_seller",
                password=self.password,
            ),
            role="seller",
        )
        self.buyer = VendingMachineUser.objects.create(
            user=User.objects.create_user(
                username="test_buyer",
                password=self.password,
            ),
            role="buyer",
        )

    def test_buy_should_fail_with_insufficient_deposit(self):
        product = Product.objects.create(
            name="Test Product",
            quantity=10,
            price=50,
            seller=self.seller,
        )
        self.buyer.deposit = 30
        self.buyer.save(update_fields=["deposit"])
        data = {"product_id": product.id}
        response = self.client.post(
            reverse("buy"),
            data,
            format="json",
            HTTP_AUTHORIZATION=create_auth_header(
                self.buyer.user.username, self.password
            ),
        )
        self.assertEqual(
            response.status_code, status.HTTP_402_PAYMENT_REQUIRED
        )

    def test_buy_should_fail_with_no_stock(self):
        product = Product.objects.create(
            name="Test Product",
            quantity=0,
            price=50,
            seller=self.seller,
        )
        self.buyer.deposit = 100
        self.buyer.save(update_fields=["deposit"])
        data = {"product_id": product.id}
        response = self.client.post(
            reverse("buy"),
            data,
            format="json",
            HTTP_AUTHORIZATION=create_auth_header(
                self.buyer.user.username, self.password
            ),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_buy_should_fail_with_invalid_product_id(self):
        Product.objects.create(
            name="Test Product",
            quantity=10,
            price=50,
            seller=self.seller,
        )
        self.buyer.deposit = 100
        self.buyer.save(update_fields=["deposit"])
        data = {"product_id": 3000}
        response = self.client.post(
            reverse("buy"),
            data,
            format="json",
            HTTP_AUTHORIZATION=create_auth_header(
                self.buyer.user.username, self.password
            ),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_buy_should_succeed_with_valid_state(self):
        product = Product.objects.create(
            name="Test Product",
            quantity=10,
            price=50,
            seller=self.seller,
        )
        self.buyer.deposit = 100
        self.buyer.save(update_fields=["deposit"])
        previous_quantity, previous_deposit = (
            product.quantity,
            self.buyer.deposit,
        )

        data = {"product_id": product.id}
        response = self.client.post(
            reverse("buy"),
            data,
            format="json",
            HTTP_AUTHORIZATION=create_auth_header(
                self.buyer.user.username, self.password
            ),
        )
        self.buyer.refresh_from_db()
        product.refresh_from_db()
        self.assertEqual(
            response.status_code,
            status.HTTP_202_ACCEPTED,
        )
        self.assertEqual(
            self.buyer.deposit,
            previous_deposit - product.price,
        )
        self.assertEqual(
            product.quantity,
            previous_quantity - 1,
        )
