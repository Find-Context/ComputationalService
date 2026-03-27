from enum import Enum


class MessageTypes(Enum):
    """
    Enum for message types.
    """

    def __str__(self):
        return str(self.value)

    # Message types for client-server communication
    AUDIO = "audio"
    DOCUMENT = "document"
    IMAGE = "image"
    TEXT = "text"
    VIDEO = "video"
