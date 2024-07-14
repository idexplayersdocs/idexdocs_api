from datetime import date, datetime

from src.repository.repo_atleta import AtletaRepo


class AtletaUpdateUseCase:
    def __init__(self, atleta_repository: AtletaRepo):
        self.atleta_repository = atleta_repository

    def execute(self, http_request: dict):
        atleta_data: dict = http_request.get('atleta')
        atleta_id: int = int(http_request.get('id'))
        
        result = self._update_atleta(atleta_id, atleta_data)

        return result

    def _update_atleta(self, atleta_id: int, atleta_data: dict) -> dict:
        date_obj: date = datetime.strptime(
        atleta_data.get('data_nascimento'), '%Y-%m-%d'
        )
        atleta_data['data_nascimento'] = date_obj

        return self.atleta_repository.update_atleta(atleta_id, atleta_data)
