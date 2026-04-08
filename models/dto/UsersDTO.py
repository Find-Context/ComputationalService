from datetime import datetime

from pydantic import BaseModel


class UsersDTO(BaseModel):
    telegram_id: int
    username: str
    first_name: str
    last_name: str
    registered_at: datetime
