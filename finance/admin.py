from django.contrib import admin

from .models import Category, Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "balance", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "user__username", "user__email")
    autocomplete_fields = ("user",)
    ordering = ("-created_at",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type_label", "user")
    list_filter = ("type",)
    search_fields = ("name", "user__username", "user__email")
    autocomplete_fields = ("user",)
    ordering = ("name",)

    @admin.display(description="Turi")
    def type_label(self, obj):
        return obj.get_type_display()
