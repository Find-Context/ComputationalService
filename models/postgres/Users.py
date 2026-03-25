from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, BigInteger, String, DateTime


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'

    telegram_id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    registered_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return (f"<User("
                f"telegram_id={self.telegram_id},"
                f" username='{self.username},"
                f" first_name='{self.first_name}',"
                f" last_name='{self.last_name}',"
                f" registered_at='{self.registered_at}"
                f"')>")
