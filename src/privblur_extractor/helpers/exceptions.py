class InitialTumblrAPIParseException(Exception):
    def __init__(self, message):
        super().__init__(message)


class TumblrErrorResponse(Exception):
    def __init__(self, message, code):
        super().__init__(
            f"Tumblr has returned an error reponse!\n"
            f"Code: {code}\n"
            f"Message: {message}"
        )
