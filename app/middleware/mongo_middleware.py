from fastapi import Request, HTTPException

from pymongo.errors import DuplicateKeyError
from core.exceptions.database_connection_error import DatabaseConnectionError


async def message_exception_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except DatabaseConnectionError as e:
        return HTTPException(status_code=500, detail=str(e))
    except DuplicateKeyError as e:
        return HTTPException(status_code=409, detail="Message with the same chatId and messageId already exists")
    except Exception as e:
        print(f"Unexpected error: {e}")
        return HTTPException(status_code=500, detail="An unexpected error occurred.")
