from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from loguru import logger

from .models.dto.base import BaseResponseStructural
from .routers import auth_router, user_router, ad_router, comment_router


class BaseResponse(JSONResponse):
    def __init__(self, content: Any, status_code: int = 200, *args, **kwargs) -> None:
        content = BaseResponseStructural(content=content, error=False, error_desc='').model_dump()
        super().__init__(content, status_code, *args, **kwargs)


def create_app(version: tuple, debug: bool = False) -> FastAPI:
    app = FastAPI(
        version='.'.join(map(str, version)),
        title='Сервис по размещению объявлений',
        default_response_class=BaseResponse,
        debug=debug,
    )

    @app.exception_handler(Exception)
    def error_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(f'{exc.__class__.__name__} {exc}')
        return JSONResponse(
            {
                'content': '',
                'error': True,
                'error_desc': f'({exc.__class__.__name__}) {exc}'
            },
        )

    @app.exception_handler(RequestValidationError)
    def bad_request(request: Request, exc: Exception) -> JSONResponse:
        logger.error(f'{exc.__class__.__name__} {exc}')
        return JSONResponse(
            {
                'content': '',
                'error': True,
                'error_desc': f'({exc.__class__.__name__}) {exc}'
            },
        )

    @app.exception_handler(ValidationError)
    def bad_request(request: Request, exc: Exception) -> JSONResponse:
        logger.error(f'{exc.__class__.__name__} {exc}')
        return JSONResponse(
            {
                'content': '',
                'error': True,
                'error_desc': f'({exc.__class__.__name__}) {exc}'
            },
        )

    app.include_router(auth_router, prefix='/api/v1')
    app.include_router(user_router, prefix='/api/v1')
    app.include_router(ad_router, prefix='/api/v1')
    app.include_router(comment_router, prefix='/api/v1')

    return app
