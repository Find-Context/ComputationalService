from .BaseModel import Base
from sqlalchemy import ForeignKey, BIGINT
from sqlalchemy.orm import relationship, mapped_column, Mapped


class UsersChats(Base):
    __tablename__ = 'users_chats'

    user_id: Mapped[BIGINT] = mapped_column(ForeignKey('users.telegram_id'), primary_key=True)
    chat_id: Mapped[BIGINT] = mapped_column(ForeignKey('chats.telegram_chat_id'), primary_key=True)

    user: Mapped["Users"] = relationship("Users", back_populates="chats")
    chat: Mapped["Chats"] = relationship("Chats", back_populates="users")

    def __repr__(self):
        return f"<UsersChats(user_id={self.user_id}, chat_id={self.chat_id})>"
