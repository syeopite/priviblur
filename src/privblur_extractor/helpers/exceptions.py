class InitialTumblrAPIParseException(Exception):
    def __init__(self, message):
        super().__init__(message)


# TODO replace 
class TumblrErrorResponse(Exception):
    def __init__(self, message, code, details):
        message = f"Tumblr has returned an error response\nCode: {code}\nMessage: {message}"

        if details:
            message += f"\nDetails: {details}" 

        super().__init__(message)

