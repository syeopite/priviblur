class InitialTumblrAPIParseException(Exception):
    def __init__(self, message):
        super().__init__(message)


# TODO replace 
class TumblrErrorResponse(Exception):
    def __init__(self, message, code, details, internal_code):
        message = f"Tumblr has returned an error response\nHTTP Code: {code}\nMessage: {message}"

        self.message = message
        self.code = code
        self.details = details
        self.internal_code = internal_code

        if details:
            message += f"\nDetails: {details}"

        if internal_code:
            message += f"\nError Code: {internal_code}"

        super().__init__(message)


class TumblrBlogNotFoundError(TumblrErrorResponse):
    pass


class TumblrRestrictedTagError(TumblrErrorResponse):
    pass


class TumblrLoginRequiredError(TumblrErrorResponse):
    pass