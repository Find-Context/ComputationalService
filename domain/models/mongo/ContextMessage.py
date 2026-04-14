from dataclasses import dataclass


@dataclass
class ContextMessageDao:
    chat_id: int
    embedding: list[float]
