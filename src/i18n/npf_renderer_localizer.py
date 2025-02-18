import functools
import gettext

import babel.dates
import babel.numbers
import npf_renderer

class NPFRendererGettextFallback(gettext.NullTranslations):
    def gettext(self, message):
        return npf_renderer.DEFAULT_LOCALIZATION["strings"][message]

    def ngettext(self, msgid1: str, msgid2: str, n: int) -> str:
        return npf_renderer.DEFAULT_LOCALIZATION["strings"][msgid1]


class NPFRendererLocalizer:
    """Localizes strings and provide formatting functions based on the given locale
    
    This class serves as a bridge to translate Priviblur's Gettext based translation system to npf-renderer's
    dict based api
    """
    def __init__(self, language, translate_func) -> None:
        self.language = language
        self.strings_localizer = NPFRendererStringsLocalizer(language, translate_func)

        self.locale_formatting  = {
            "duration": {"__default__": functools.partial(babel.dates.format_timedelta, threshold=1.1, locale=language)},
            "datetime": {"__default__": functools.partial(babel.dates.format_datetime, format=f"short", locale=language)},
            "decimal": {"__default__": functools.partial(babel.numbers.format_decimal, locale=language)},
        }

    def __getitem__(self, key : str):
        if key == "strings":
            return self.strings_localizer
        return self.locale_formatting


class NPFRendererStringsLocalizer:
    def __init__(self, language, translate_func):
        self.language = language

        self.translate_func = translate_func

    def translate(self, key, *args):
        key = f"npf_renderer_{key}"
        return self.translate_func(self.language, key, *args)

    def __getitem__(self, key : str):
        if key[:7] == "plural_":
            return lambda number : self.translate(key[7:], number)
        else:
            return self.translate(key)
