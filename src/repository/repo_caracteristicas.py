from datetime import date, datetime

from sqlmodel import func, select

from src.repository.model_objects import (
    CaracteristicaAtacante,
    CaracteristicaFisica,
    CaracteristicaGoleiro,
    CaracteristicaLateral,
    CaracteristicaMeia,
    CaracteristicaVolante,
    CaracteristicaZagueiro,
)

from .base_repo import create_session


class CaracteristicasRepo:
    MODELS = {
        'fisico': CaracteristicaFisica,
        'zagueiro': CaracteristicaZagueiro,
        'lateral': CaracteristicaLateral,
        'goleiro': CaracteristicaGoleiro,
        'volante': CaracteristicaVolante,
        'atacante': CaracteristicaAtacante,
        'meia': CaracteristicaMeia,
    }

    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_dict_from_object(
        self, result: list, model_fields: list, model_name: str
    ) -> list[dict]:
        if not result:
            return [], model_name

        # Determina os campos existentes utilizando a primeira row como amostra
        existing_fields = {
            field.name: field
            for field in model_fields
            if hasattr(result[0], field.name)
        }

        # Criar um dicionário fazendo o convertendo campos datetime para string
        dicts = []
        for row in result:
            row_dict = {}
            for field_name, field in existing_fields.items():
                value = getattr(row, field_name)
                if isinstance(value, datetime):
                    row_dict[field_name] = value.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(value, date):
                    row_dict[field_name] = value.strftime('%Y-%m-%d')
                else:
                    row_dict[field_name] = value
            dicts.append(row_dict)

        return dicts, model_name

    def _get_model(self, model_name: str):

        if model_name not in self.MODELS:
            raise ValueError(f'Característica não é válida: {model_name}')

        return self.MODELS.get(model_name)

    def list_caracteristica(self, atleta_id: int, filters: dict):
        model = self._get_model(filters.get('model'))

        with self.session_factory() as session:
            query = select(model).where(model.atleta_id == atleta_id)

            dicts, model_name = self._create_dict_from_object(
                session.exec(query).all(),
                model.__table__.columns,
                model.__name__,
            )

            return dicts, model_name

    def create_caracteristica(self, data: dict, model_name: str):
        model = self._get_model(model_name)

        with self.session_factory() as session:
            data = model(**data)
            session.add(data)
            session.commit()
            session.refresh(data)
            return {'id': data.id}
