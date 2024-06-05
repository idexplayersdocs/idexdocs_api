class TokenInvalidError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.name = 'InvalidToken'
        self.status_code = 401
