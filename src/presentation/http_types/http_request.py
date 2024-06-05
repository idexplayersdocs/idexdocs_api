"""Modulo para adaptação do objeto request do framework específico para o
core da aplicação
"""

from dataclasses import dataclass


@dataclass
class HttpRequest:
    headers: str = None
    data: str = None
    json: str = None
    query_params: str = None
    path_params: str = None
    url: str = None
    files: bytes = None
