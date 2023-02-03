from django.urls import path

from . import views

urlpatterns = [
    # User CRUD
    path(
        "users/",
        views.UserView.as_view({"get": "list", "post": "create"}),
        name="user-list",
    ),
    path(
        "users/<int:pk>/",
        views.UserView.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="user-detail",
    ),
    # Product CRUD
    path(
        "products/",
        views.ProductView.as_view({"get": "list", "post": "create"}),
        name="product-list",
    ),
    path(
        "products/<int:pk>/",
        views.ProductView.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="product-detail",
    ),
]
