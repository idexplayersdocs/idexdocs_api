from fastapi import Request
from pydantic import BaseModel

from src.schemas.caracteristica import *

CARACTERISTICAS_SCHEMA = {
    'fisico': CaracteristicaFisicaCreateSchema,
    'zagueiro': CaracteristicaZagueiroCreateSchema,
    'lateral': CaracteristicaLateralCreateSchema,
    'goleiro': CaracteristicaGoleiroCreateSchema,
    'volante': CaracteristicaVolanteCreateSchema,
    'atacante': CaracteristicaAtacanteCreateSchema,
    'meia': CaracteristicaMeiaCreateSchema,
}


async def validate_schema(request: Request, default_schema: BaseModel = None):
    is_post_or_put = request.method in ['POST', 'PUT']
    # Check if it's a relevant method and there is no form data.
    if is_post_or_put and not await request.form():
        request_body = await request.json()

        # Validate schema for POST or PUT requests.
        if default_schema:
            default_schema.model_validate(request_body)

        # Specific validation for creating a caracteristica.
        if request.method == 'POST' and '/create/caracteristica' == request.url.path:
            caracteristica_tipo = request_body.get('caracteristica')

            if caracteristica_tipo not in CARACTERISTICAS_SCHEMA:
                raise ValueError(f'Característica não é válida: {caracteristica_tipo}')

            # Get the specific schema and validate.
            specific_schema = CARACTERISTICAS_SCHEMA[caracteristica_tipo]
            specific_schema.model_validate(request_body)

