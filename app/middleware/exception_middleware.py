from fastapi import Request
from sqlalchemy.exc import DataError

from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from core.exceptions import DatabaseConnectionError, DuplicatedPrimaryKeyError


class GlobalExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except DatabaseConnectionError as e:
            print(f"Database connection error: {e}")

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": "Database connection error: " + str(e)}, )
        except DuplicatedPrimaryKeyError as e:
            print(f"Error duplicated primary keys: {e}")

            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"message": "Error duplicated primary keys: " + str(e)}, )
        except DataError as e:
            print(f"Invalid data error: {e}")

            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Invalid data error: " + str(e)},
            )
        except Exception as e:
            print(f"Unexpected error: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": "Unexpected error: " + str(e)},
            )
