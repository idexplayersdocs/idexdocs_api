class RedisExceptionError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.name = 'RedisException'
        self.status_code = 500
