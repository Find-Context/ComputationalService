from . import *


class Base(DeclarativeBase):
    pass


class Chats(Base):
    __tablename__ = 'chats'

    telegram_chat_id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return (f'<Chat('
                f'telegram_chat_id={self.telegram_chat_id},'
                f' title="{self.title}",'
                f' created_at="{self.created_at}"'
                f')>')
