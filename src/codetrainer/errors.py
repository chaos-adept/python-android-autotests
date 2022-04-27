class CompilationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class VerificationFailedError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class VerificationFailedError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class JavaRunFailedError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
