from fastapi import Request
from fastapi.responses import JSONResponse

from src.error.error_handler import handle_errors
from src.main.adapters.request_adapter import request_adapter
from src.main.composers.files_download_composer import (
    multiple_files_download_composer,
)


async def multiple_files_download(request: Request):
    try:
        http_response = await request_adapter(
            request, multiple_files_download_composer()
        )
    except Exception as exc:
        http_response = handle_errors(exc)
    return JSONResponse(http_response.body, http_response.status_code)
