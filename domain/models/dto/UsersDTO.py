from datetime import datetime

from pydantic import BaseModel


class UsersDTO(BaseModel):
    telegram_id: int
    username: str
    first_name: str | None = None
    last_name: str | None = None
    registered_at: datetime
