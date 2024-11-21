from typing import Any, Optional


class BrickError(Exception):

    """
    Raised when a brick-related error occurs.

    Attributes:
        message (str): A human-readable error message.
        culprit (str | int | None): The brick that caused the error, if applicable.
    """

    def __init__(self, message: str, culprit: Optional[str | int] = None):

        super().__init__()
        self.message: str = message
        self.culprit: Optional[str, int] = culprit


    def __str__(self) -> str:
        if self.culprit is None:
            return self.message
        # else:
        return f"{self.message} (from brick {self.culprit!r})"


    def __reduce__(self) -> tuple[Any, tuple[str, Optional[str | int]]]:

        return self.__class__, (self.message, self.culprit)


class FontError(Exception):
    pass
