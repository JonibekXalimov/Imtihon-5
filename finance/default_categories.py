DEFAULT_CATEGORIES = [
    ("Oylik", "income"),
    ("Avans", "income"),
    ("Kunlik ish haqi", "income"),
    ("Yo'lkira", "expense"),
    ("Tushlik", "expense"),
    ("Salomatlik", "expense"),
]

DEFAULT_WALLETS = [
    ("Naqd pul", 0),
    ("Karta", 0),
    ("Valyuta", 0),
]


def create_default_categories_for_user(user):
    from .models import Category

    for name, category_type in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(
            user=user,
            name=name,
            type=category_type,
        )


def create_default_wallets_for_user(user):
    from .models import Wallet

    for name, balance in DEFAULT_WALLETS:
        Wallet.objects.get_or_create(
            user=user,
            name=name,
            defaults={"balance": balance},
        )
