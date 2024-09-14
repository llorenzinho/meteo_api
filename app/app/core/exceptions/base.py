from http import HTTPStatus
from fastapi.responses import JSONResponse
from app.core.logger import get_logger


logger = get_logger()


class ErrorOut:
    message: str

    def __init__(self, message):
        self.message = message


def base_ex_handler(_, err: Exception):
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content='Internal Server Error',
    )
