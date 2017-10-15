class VaultError(Exception):
    def __init__(self, message=None, errors=None, response=None):
        self.response = response

        if not errors and response and 'application/json' in response.headers['Content-Type']:
            # Try to guess the error message from the response
            json = response.json()
            if 'errors' in json:
                errors = json['errors']

        if errors:
            message = ', '.join(errors)

        self.errors = errors

        super(VaultError, self).__init__(message)

class InvalidRequest(VaultError):
    pass

class Unauthorized(VaultError):
    pass

class Forbidden(VaultError):
    pass

class InvalidPath(VaultError):
    pass

class RateLimitExceeded(VaultError):
    pass

class InternalServerError(VaultError):
    pass

class VaultNotInitialized(VaultError):
    pass

class VaultDown(VaultError):
    pass

class UnexpectedError(VaultError):
    pass
