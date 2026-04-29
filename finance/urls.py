from django.urls import path
from .views import (
    WalletListView,
    WalletCreateView,
    WalletUpdateView,
    WalletDeleteView,
    CategoryListView,
    CategoryCreateView,
)

urlpatterns = [
    path("wallets/", WalletListView.as_view(), name="wallet-list"),
    path("wallets/create/", WalletCreateView.as_view(), name="wallet-create"),
    path("wallets/<int:pk>/update/", WalletUpdateView.as_view(), name="wallet-update"),
    path("wallets/<int:pk>/delete/", WalletDeleteView.as_view(), name="wallet-delete"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/create/", CategoryCreateView.as_view(), name="category-create"),
]
