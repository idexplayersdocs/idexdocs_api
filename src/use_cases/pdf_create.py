from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_caracteristicas import CaracteristicasRepo
from src.repository.repo_clube import ClubeRepo
from src.repository.repo_competicao import CompeticaoRepo
from src.repository.repo_controle import ControleRepo
from src.repository.repo_lesao import LesaoRepo
from src.repository.repo_observacao import ObservacaoRepo
from src.repository.repo_relacionamento import RelacionamentoRepo
from src.use_cases.caracteristica_list import CaracteristicaListUseCase


class PdfCreateUseCase:
    def __init__(
        self,
        *,
        clube_repository: ClubeRepo,
        atleta_repository: AtletaRepo,
        lesao_repository: LesaoRepo,
        controle_repository: ControleRepo,
        competicao_repository: CompeticaoRepo,
        observacao_repository: ObservacaoRepo,
        caracteristica_repository: CaracteristicasRepo,
        caracteristica_use_case: CaracteristicaListUseCase,
        relacionamento_repository: RelacionamentoRepo,
    ) -> None:
        self.clube_repository = clube_repository
        self.lesao_repository = lesao_repository
        self.atleta_repository = atleta_repository
        self.controle_repository = controle_repository
        self.observacao_repository = observacao_repository
        self.competicao_repository = competicao_repository
        self.caracteristica_use_case = caracteristica_use_case
        self.relacionamento_repository = relacionamento_repository
        self.caracteristica_repository = caracteristica_repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = int(http_request.path_params.get('id'))
        filters: dict = dict(http_request.query_params.items())
        # Adicionando informações no filtro para gerenciar a impressão do PDF
        filters.update({'page': 1, 'per_page': 1000, 'model': 'fisico'})
        
        # Recuperando informações do atleta
        atleta = self._get_atleta(atleta_id)
        # Recuperando toads informações inerentes ao atleta
        _, clubes = self.clube_repository.list_clube(atleta_id, filters)
        _, lesoes = self.lesao_repository.list_lesao(atleta_id, filters)
        _, controles = self.controle_repository.list_controle(atleta_id, filters)
        _, competicoes = self.competicao_repository.list_competicao(atleta_id, filters)
        caracteristicas_fisicas, _ = self.caracteristica_repository.list_caracteristica(atleta_id, filters)
        observacoes_desempenho = self.observacao_repository.list_observacao(atleta_id, filters={'tipo': 'desempenho'})
        observacoes_relacionamento = self.observacao_repository.list_observacao(atleta_id, filters={'tipo': 'relacionamento'})

        # Dicionário com dados iniciais
        data = {
            'atleta': atleta,
            'clube': clubes,
            'lesao': lesoes,
            'controle': controles,
            'competicao': competicoes,
            'observacoes_relacionamento': observacoes_relacionamento,
            'observacoes_desempenho': observacoes_desempenho,
            'caracteristicas_fisicas': caracteristicas_fisicas,
        }

        # Gerenciando permissões para disponibilizar informações sensíveis
        permissoes = filters.get('permissoes', [])
        if 'create_desempenho' in permissoes:
            # Recuperando informações específicas da posição do atleta
            filters.update({'model': atleta.get('posicao_primaria')})
            http_request.query_params = filters
            caracteristicas_posicao = self.caracteristica_use_case.execute(http_request)
            del caracteristicas_posicao['type']
            data.update({'caracteristicas_posicao': caracteristicas_posicao['data']})

        if 'create_relacionamento' in permissoes:    
            _, relacionamentos = self.relacionamento_repository.list_relacionamento(atleta_id, filters)
            data.update({'relacionamento': relacionamentos})

        return data
    
    def _get_atleta(self, atleta_id: int) -> dict:
        atleta = self.atleta_repository.get_atleta(atleta_id)

        if atleta is not None:
            return atleta

        raise NotFoundError('Atleta não encontrado')
