from datetime import datetime
from typing import List

from sqlalchemy.testing.schema import mapped_column

from .BaseModel import Base
from sqlalchemy import String, DateTime, BIGINT
from sqlalchemy.orm import Mapped, relationship

from .UsersChats import UsersChats


class Users(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    chats: Mapped[List["UsersChats"]] = relationship("UsersChats", back_populates="user")

    def __repr__(self):
        return (f"<User("
                f"telegram_id={self.telegram_id},"
                f" username='{self.username},"
                f" first_name='{self.first_name}',"
                f" last_name='{self.last_name}',"
                f" registered_at='{self.registered_at}"
                f"')>")
