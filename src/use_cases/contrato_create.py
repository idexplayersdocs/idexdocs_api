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
        contrato_data: dict = dict(http_request.json)
        atleta_id: int = contrato_data.get('atleta_id')
        contrato_id: int = contrato_data.get('contrato_sub_tipo_id')

        self._check_contrato_already_exists(atleta_id, contrato_id)

        return self._create_contrato(contrato_data)

    def _check_contrato_already_exists(self, atleta_id: int, contrato_id: int):
        contrato: Contrato = self.contrato_repository.get_contrato_by_tipo_e_atleta(atleta_id, contrato_id)
        if contrato is not None:
            raise ContratoExistente(f'Contrato {contrato.nome} já existe para o atleta')

    def _create_contrato(self, contrato_data: dict):
        contrato = self.contrato_repository.create_contrato(
            contrato_data
        )

        return contrato
