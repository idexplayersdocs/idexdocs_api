from fastapi import Request
from fastapi.responses import JSONResponse

from src.error.error_handler import handle_errors
from src.main.adapters.request_adapter import request_adapter
from src.main.composers.controle_delete_composer import (
    controle_delete_composer,
)


async def controle_delete(request: Request):
    try:
        http_response = await request_adapter(
            request, controle_delete_composer()
        )
    except Exception as exc:
        http_response = handle_errors(exc)
    return JSONResponse(http_response.body, http_response.status_code)
