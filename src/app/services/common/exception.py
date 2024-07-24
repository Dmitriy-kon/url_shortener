class ServiceError(Exception):
    """Base class for all buisness layer errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class UserNotFoundError(ServiceError):
    pass
