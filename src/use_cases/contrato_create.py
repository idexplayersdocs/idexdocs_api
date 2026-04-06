from src.error.types.contrato_existente import ContratoExistente
from src.presentation.http_types.http_request import HttpRequest
from src.repository.model_objects import Contrato
from src.repository.repo_contrato import ContratoRepo


class ContratoCreateUseCase:
    def __init__(
        self,
        contrato_repository: ContratoRepo,
    ):
        self.contrato_repository = contrato_repository

    def execute(self, http_request: HttpRequest):
        # Detect JSON vs FormData #TODO: Refactor this to a separate function and add tests
        if http_request.json:
            contrato_data = dict(http_request.json)
        else:
            form = http_request.files
            contrato_data = {
                'atleta_id': int(form.get('atleta_id')),
                'contrato_sub_tipo_id': int(form.get('contrato_sub_tipo_id')),
                'data_inicio': form.get('data_inicio'),
                'data_termino': form.get('data_termino'),
                'observacao': form.get('observacao') or None,
            }

        atleta_id: int = contrato_data.get('atleta_id')
        contrato_sub_tipo_id: int = contrato_data.get('contrato_sub_tipo_id')

        self._check_contrato_already_exists(atleta_id, contrato_sub_tipo_id)

        return self._create_contrato(contrato_data)

    def _check_contrato_already_exists(self, atleta_id: int, contrato_id: int):
        contrato: Contrato = self.contrato_repository.get_contrato_by_tipo_e_atleta(atleta_id, contrato_id)
        if contrato is not None:
            raise ContratoExistente(f'Contrato {contrato.nome} já existe para o atleta')

    def _create_contrato(self, contrato_data: dict):
        contrato = self.contrato_repository.create_contrato(contrato_data)
        return contrato
