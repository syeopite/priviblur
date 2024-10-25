import sys
import gettext
import typing

import sanic

from .i18n_data import LOCALE_DATA


class Language:
    """Stores metadata about supported translations"""
    def __init__(self, locale, gettext_instance,) -> None:
        self.locale = locale
        self.instance = gettext_instance

        self.name, self.translation_percentage = LOCALE_DATA[locale]

SUPPORTED_LANGUAGES = [
    "en_US", "cs_CZ", "fr", "ja", "uk"
]

SUPPORTED_LANGUAGES.sort()


def initialize_locales() -> typing.Mapping[str, gettext.GNUTranslations]:
    """Initializes locales into GNUTranslations instances"""
    # Initialize locales
    try:
        languages = {}
        for locale in SUPPORTED_LANGUAGES:
            instance = gettext.translation("priviblur", localedir="locales", languages=(locale,))

            languages[locale] = Language(locale, instance)
    except FileNotFoundError as e:
        print(
            'Error: Unable to find locale files. '
            'Did you forget to compile them?'
        )

        sys.exit()
    except Exception as e:
        raise e

    return languages


def translate(language : str, id : str, number : int|float = None,
              substitution : str = None) -> str:
    app = sanic.Sanic.get_app("Priviblur")

    gettext_instance = app.ctx.LANGUAGES[language].instance

    if number is not None:
        translated = gettext_instance.ngettext(id, f"{id}_plural", number)
    else:
        translated = gettext_instance.gettext(id)

    if substitution:
        translated = translated.format(substitution)

    return translated 