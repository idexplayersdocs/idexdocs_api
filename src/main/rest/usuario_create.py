from fastapi import Request
from fastapi.responses import JSONResponse

from src.error.error_handler import handle_errors
from src.main.adapters.request_adapter import request_adapter
from src.main.composers.usuario_create_composer import usuario_create_composer
from src.schemas.usuario import UsuarioCreateSchema
from src.validators.validate_schema import validate_schema


async def usuario_create(request: Request):
    try:
        await validate_schema(request, UsuarioCreateSchema)
        http_response = await request_adapter(
            request, usuario_create_composer()
        )
    except Exception as exc:
        http_response = handle_errors(exc)
    return JSONResponse(http_response.body, http_response.status_code)
