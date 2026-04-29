from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "transaction_type_label",
        "amount",
        "wallet",
        "category",
        "created_at",
    )
    list_filter = ("transaction_type", "created_at", "category")
    search_fields = (
        "user__username",
        "user__email",
        "wallet__name",
        "category__name",
    )
    autocomplete_fields = (
        "user",
        "wallet",
        "category",
    )
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_select_related = (
        "user",
        "wallet",
        "category",
    )

    @admin.display(description="Turi")
    def transaction_type_label(self, obj):
        return obj.get_transaction_type_display()
