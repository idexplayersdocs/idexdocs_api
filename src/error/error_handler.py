import logging

from pydantic import ValidationError

from src.presentation.http_types.http_response import HttpResponse

from .types import (
    BadRequestError,
    ClubeAtivoExistente,
    ContratoExistente,
    ExpiredTokenError,
    NotFoundError,
    SenhaInvalida,
    TokenInvalidError,
    UsuarioExistente,
    UsuarioNaoEncontrado,
)

logger = logging.getLogger(__name__)


def handle_errors(error: Exception) -> HttpResponse:
    if isinstance(
        error,
        (
            BadRequestError,
            NotFoundError,
            ExpiredTokenError,
            TokenInvalidError,
            ClubeAtivoExistente,
            UsuarioExistente,
            UsuarioNaoEncontrado,
            SenhaInvalida,
            ContratoExistente,
        ),
    ):
        logger.info(f'Handling known error: {error.name}')
        return HttpResponse(
            status_code=error.status_code,
            body={'errors': [{'title': error.name, 'message': error.message}]},
        )

    elif isinstance(error, (ValidationError,)):

        def format_pydantic_error(error):
            body = error.errors()[0]
            body_loc = body['loc'][0] if len(body['loc']) > 0 else body['loc']
            return f'{body_loc}: {body["msg"]}'

        logger.info('Handling ValidationError')
        return HttpResponse(
            status_code=422,
            body={
                'errors': [
                    {
                        'title': 'ValidationError',
                        'message': format_pydantic_error(error),
                    }
                ]
            },
        )

    logger.warning('Handling unknown error, returning ServerError')
    return HttpResponse(
        status_code=500,
        body={'errors': [{'title': 'ServerError', 'message': str(error)}]},
    )
