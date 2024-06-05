from fastapi import Request
from fastapi.responses import JSONResponse

from src.error.error_handler import handle_errors
from src.main.adapters.request_adapter import request_adapter
from src.main.composers.relacionamento_create_composer import (
    relacionamento_create_composer,
)
from src.schemas.relacionamento import RelacionamentoCreateSchema
from src.validators.validate_schema import validate_schema


async def relacionamento_create(request: Request):
    try:
        await validate_schema(request, RelacionamentoCreateSchema)
        http_response = await request_adapter(
            request, relacionamento_create_composer()
        )
    except Exception as exc:
        http_response = handle_errors(exc)
    return JSONResponse(http_response.body, http_response.status_code)
