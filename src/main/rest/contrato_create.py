from fastapi import Request
from fastapi.responses import JSONResponse

from src.error.error_handler import handle_errors
from src.main.adapters.request_adapter import request_adapter
from src.main.composers.contrato_create_composer import (
    contrato_create_composer,
)
from src.schemas.contrato import ContratoCreateSchema
from src.validators.validate_schema import validate_schema


async def contrato_create(request: Request):
    try:
        await validate_schema(request, ContratoCreateSchema)
        http_response = await request_adapter(request, contrato_create_composer())
    except Exception as exc:
        http_response = handle_errors(exc)
    return JSONResponse(http_response.body, http_response.status_code)
