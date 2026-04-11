from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import Column, BIGINT, String, DateTime
from typing import List

from .BaseModel import Base
from .UsersChats import UsersChats


class Chats(Base):
    __tablename__ = 'chats'

    telegram_chat_id = Column(BIGINT, primary_key=True, unique=True, nullable=False)
    title = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)

    users: Mapped[List["UsersChats"]] = relationship("UsersChats", back_populates="chat")

    def __repr__(self):
        return (f'<Chat('
                f'telegram_chat_id={self.telegram_chat_id},'
                f' title="{self.title}",'
                f' created_at="{self.created_at}"'
                f')>')
