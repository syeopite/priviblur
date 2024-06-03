import datetime
import dataclasses
import urllib.parse

VERSION = 1

@dataclasses.dataclass
class UserPreferences:
    # See DefaultUserPreferences in config/user_preferences.py
    language: str
    theme: str

    # Tracks major revisions of the settings cookie
    # Only bump in case of breaking changes.
    version: int = 1

    def update_from_forms(self, request):
        return self._update(request, request.form)

    def update_from_query(self, request):
        return self._update(request, request.args)

    def _update(self, request, raw_new_prefs):
        language = raw_new_prefs.get("language", request.app.ctx.PRIVIBLUR_CONFIG.default_user_preferences.language)
        if language not in request.app.ctx.SUPPORTED_LANGUAGES:
            language = request.app.ctx.PRIVIBLUR_CONFIG.default_user_preferences.language

        self.language = language
        request.ctx.language = self.language

        self.theme = raw_new_prefs.get("theme", request.app.ctx.PRIVIBLUR_CONFIG.default_user_preferences.theme)

    def to_url_encoded(self):
        return urllib.parse.urlencode(dataclasses.asdict(self))

    def to_cookie(self, request):
        if request.scheme == "http":
            secure = False
        else:
            secure = True

        cookie = {
            "key": "settings",
            "value": self.to_url_encoded(),
            "secure": secure,
            "max_age": 31540000
        }

        if request.app.ctx.PRIVIBLUR_CONFIG.deployment.domain:
            cookie["domain"] = request.app.ctx.PRIVIBLUR_CONFIG.deployment.domain

        return cookie
