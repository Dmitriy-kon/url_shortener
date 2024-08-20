class ServiceError(Exception):
    """Base class for all buisness layer errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class UserNotFoundError(ServiceError):
    pass


class UserAlreadyExistsError(ServiceError):
    pass


class UserPasswordNotMatchError(ServiceError):
    pass


class UserIsNotAuthorizedError(ServiceError):
    pass


class UrlAllreadyExistsError(ServiceError):
    pass

class UrlNotFoundError(ServiceError):
    pass
