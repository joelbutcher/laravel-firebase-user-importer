class DbConnectionError(Exception):
    def __init__(self, exc: Exception, max_retries: int):
        self.args = exc.args
        self.error_type = type(exc)
        self.max_retries = max_retries
        self.error_object = self._error_object()

    def _error_object(self):
        return {
            "error": "Could not connect to database.",
            "code": self.args[0],
            "connection_attempts": self.max_retries,
            "type": str(self.error_type),
        }
