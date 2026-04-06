from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_contrato import ContratoRepo


class ContratoUpdateUseCase:
    def __init__(
        self,
        contrato_repository: ContratoRepo,
    ):
        self.contrato_repository = contrato_repository

    def execute(self, http_request: HttpRequest):
        if http_request.json:
            contrato_data = dict(http_request.json)
        else:
            form = http_request.files
            contrato_data = {
                'contrato_id': int(form.get('contrato_id')),
                'data_inicio': form.get('data_inicio'),
                'data_termino': form.get('data_termino'),
                'observacao': form.get('observacao') or None,
                'ativo': form.get('ativo', 'true').lower() in ('true', '1', 'yes'),
            }

        return self._update_contrato(contrato_data)

    def _update_contrato(self, contrato_data: dict):
        contrato = self.contrato_repository.update_contrato(contrato_data)
        return contrato
