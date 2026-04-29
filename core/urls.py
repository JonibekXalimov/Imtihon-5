from django.urls import path
from .views import DashboardView, ReportsView, set_language_view

urlpatterns = [
    path("", DashboardView.as_view(), name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("reports/", ReportsView.as_view(), name="reports"),
    path("language/<str:language>/", set_language_view, name="set-language"),
]
