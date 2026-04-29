from .i18n import SUPPORTED_LANGUAGES, TEXT, get_language


def app_language(request):
    language = get_language(request)

    return {
        "app_language": language,
        "app_languages": SUPPORTED_LANGUAGES,
        "t": TEXT[language],
    }
