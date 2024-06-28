import sys
import gettext
import typing

import babel
import sanic

SUPPORTED_LANGUAGES = [
    "en_US", "cs_CZ", "fr"
]

SUPPORTED_LANGUAGES.sort()

LANGUAGE_NAMES = {
    locale : babel.Locale.parse(locale).get_language_name().capitalize() for locale in SUPPORTED_LANGUAGES
}

def initialize_locales() -> typing.Mapping[str, gettext.GNUTranslations]:
    """Initializes locales into GNUTranslations instances"""
    # Initialize locales
    try:
        gettext_instances = {}
        for language in SUPPORTED_LANGUAGES:
            gettext_instances[language] = gettext.translation(
                "priviblur", localedir="locales", languages=(language,)
            )
    except FileNotFoundError as e:
        print(
            'Error: Unable to find locale files. '
            'Did you forget to compile them?'
        )

        sys.exit()
    except Exception as e:
        raise e

    return gettext_instances


def translate(language : str, id : str, number : int|float = None,
              substitution : str = None) -> str:
    app = sanic.Sanic.get_app("Priviblur")

    gettext_instance = app.ctx.GETTEXT_INSTANCES[language]

    if number is not None:
        translated = gettext_instance.ngettext(id, f"{id}_plural", number)
    else:
        translated = gettext_instance.gettext(id)

    if substitution:
        translated = translated.format(substitution)

    return translated 