from django.urls import path
from .views import (
    TransactionListView,
    AddIncomeView,
    SpendView,
)

app_name = "transactions"

urlpatterns = [
    path("", TransactionListView.as_view(), name="list"),
    path("add-income/", AddIncomeView.as_view(), name="add-income"),
    path("spend/", SpendView.as_view(), name="spend"),
]
