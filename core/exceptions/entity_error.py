class DuplicatedPrimaryKeyError(Exception):
    def __init__(self, message: str = "Primary key already exists."):
        self.message = message
        super().__init__(self.message)
