from fastapi import APIRouter

from src.main.rest.atleta_create import atleta_create
from src.main.rest.atleta_detail import atleta_detail
from src.main.rest.atleta_list import atleta
from src.main.rest.atleta_update import atleta_update
from src.main.rest.caracteristica_create import caracteristica_create
from src.main.rest.caracteristica_list import caracteristica
from src.main.rest.clube_create import clube_create
from src.main.rest.clube_list import clube
from src.main.rest.competicao_create import competicao_create
from src.main.rest.competicao_list import competicao
from src.main.rest.contrato_create import contrato_create
from src.main.rest.contrato_list import contrato_list
from src.main.rest.contrato_tipo_list import contrato_tipo_list
from src.main.rest.contrato_update import contrato_update
from src.main.rest.contrato_versao_list import contrato_versao_list
from src.main.rest.controle_create import controle_create
from src.main.rest.controle_list import controle
from src.main.rest.file_download import file_download
from src.main.rest.file_upload import file_upload
from src.main.rest.files_delete import file_delete
from src.main.rest.files_download import multiple_files_download
from src.main.rest.files_update import imagem_update
from src.main.rest.files_upload import multiple_files_upload
from src.main.rest.lesao_create import lesao_create
from src.main.rest.lesao_list import lesao
from src.main.rest.observacao_create import observacao_create
from src.main.rest.observacao_list import observacao
from src.main.rest.pdf_create import pdf_create
from src.main.rest.relacionamento_create import relacionamento_create
from src.main.rest.relacionamento_list import relacionamento
from src.main.rest.token import token
from src.main.rest.usuario_create import usuario_create
from src.main.rest.usuario_list import usuario_list
from src.main.rest.usuario_update import usuario_update
from src.main.rest.usuario_update_password import usuario_update_password
from src.main.rest.video_delete import video_delete
from src.main.rest.video_list import video_list
from src.main.rest.video_update import video_update
from src.main.rest.video_upload import video_upload
from src.schemas.atleta import (
    AtletaCreateResponse,
    AtletaCreateSchema,
    AtletaUpdateSchema,
)
from src.schemas.caracteristica import CaracteristicaCreateResponse
from src.schemas.clube import ClubeCreateResponse, ClubeCreateSchema
from src.schemas.competicao import (
    CompeticaoCreateResponse,
    CompeticaoCreateSchema,
)
from src.schemas.contrato import (
    ContratoCreateResponse,
    ContratoCreateSchema,
    ContratoTipoResponse,
    ContratoUpdateSchema,
)
from src.schemas.controle import (
    ControleCreateResponse,
    ControleCreateSchema,
    ControleListResponse,
)
from src.schemas.file_upload import FileUpdateSchema
from src.schemas.lesao import LesaoCreateResponse, LesaoCreateSchema
from src.schemas.observacao import (
    ObservacaoCreateResponse,
    ObservacaoCreateSchema,
    ObservacaoListResponse,
)
from src.schemas.relacionamento import (
    RelacionamentoCreateSchema,
    RelacionamentoResponse,
)
from src.schemas.token import Token
from src.schemas.usuario import (
    UsuarioCreateResponse,
    UsuarioUpdatePasswordResponse,
    UsuarioUpdateResponse,
    UsuarioUpdateSchema,
)
from src.schemas.video import VideoCreateSchema, VideoUpdateSchema

router = APIRouter()

router.add_api_route(
    '/usuario/create',
    endpoint=usuario_create,
    response_model=UsuarioCreateResponse,
    tags=['Usuário'],
    methods=['POST'],
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para login de usuário',
                            'description': 'usuario_tipo_id: 1 - admim 2 - treinador 3 - externo',
                            'value': {
                                'nome': 'Nome completo',
                                'email': 'email@cloud.com',
                                'password': 'teste1234',
                                'usuario_tipo_id': '1',
                            },
                        }
                    },
                }
            },
            'required': True,
        },
    },
)

router.add_api_route(
    '/usuario/update',
    endpoint=usuario_update,
    response_model=UsuarioUpdateResponse,
    tags=['Usuário'],
    methods=['PUT'],
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': UsuarioUpdateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para atualização de usuário',
                            'value': {
                                'id': 1,
                                'nome': 'Nome completo',
                                'email': 'email@cloud.com',
                                'usuario_tipo_id': '1',
                            },
                        }
                    },
                }
            },
            'required': True,
        },
    },
)

router.add_api_route(
    '/usuario/update/password',
    endpoint=usuario_update_password,
    response_model=UsuarioUpdatePasswordResponse,
    tags=['Usuário'],
    methods=['PUT'],
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': UsuarioUpdateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para atualização de senha',
                            'value': {
                                'id': 1,
                                'password': 'teste1234',
                                'new_password': 'nova_senha',
                            },
                        }
                    },
                }
            },
            'required': True,
        },
    },
)

router.add_api_route(
    '/auth/token',
    endpoint=token,
    response_model=Token,
    tags=['Token'],
    methods=['POST'],
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para login de usuário',
                            'value': {
                                'email': 'emaill@cloud.com',
                                'password': 'teste1234',
                            },
                        }
                    },
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/create/atleta',
    endpoint=atleta_create,
    tags=['Atleta'],
    methods=['POST'],
    response_model=AtletaCreateResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': AtletaCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de atleta',
                            'value': {
                                'nome': 'Igor',
                                'data_nascimento': '1985-03-11',
                                'clube': {
                                    'nome': 'SIGA SPORTS',
                                    'data_inicio': '2024-05-01',
                                },
                                'contrato_clube': {
                                    'contrato_sub_tipo_id': 1,
                                    'data_inicio': '2024-05-01',
                                    'data_fim': '2025-05-01',
                                    'observacao': 'null',
                                },
                                'contrato_empresa': {
                                    'contrato_sub_tipo_id': 2,
                                    'data_inicio': '2024-05-01',
                                    'data_fim': '2025-05-01',
                                    'observacao': 'null',
                                },
                                'posicao_primaria': 'atacante',
                                'posicao_secundaria': 'null',
                                'posicao_terciaria': 'null',
                            },
                        }
                    },
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/update/atleta/{id}',
    endpoint=atleta_update,
    tags=['Atleta'],
    methods=['PUT'],
    response_model=AtletaCreateResponse,
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            }
        ],
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': AtletaUpdateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de atleta',
                            'value': {
                                'nome': 'Atleta',
                                'data_nascimento': '2000-01-01',
                                'posicao_primaria': 'atacante',
                                'posicao_secundaria': 'volante',
                                'posicao_terciaria': 'null',
                                'ativo': False,
                            },
                        }
                    },
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/atleta',
    endpoint=atleta,
    tags=['Atleta'],
    methods=['GET'],
    openapi_extra={
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 2,
                            'type': 'Controle',
                            'data': [
                                {
                                    'nome': 'Atleta 1',
                                    'data_nascimento': '1980-09-21',
                                    'posicao_primaria': 'atacante',
                                    'posicao_secundaria': 'meia',
                                    'posicao_terciaria': None,
                                    'clube_atual': 'Clube 1',
                                },
                                {
                                    'nome': 'Atleta 2',
                                    'data_nascimento': '1985-03-11',
                                    'posicao_primaria': 'Goleiro',
                                    'posicao_secundaria': None,
                                    'posicao_terciaria': None,
                                    'clube_atual': 'Clube 1a',
                                },
                            ],
                        }
                    }
                },
            },
            '404': {
                'description': 'Not found',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'NotFound',
                                    'message': 'Não existem atletas cadastrados',
                                }
                            ]
                        }
                    }
                },
            },
        },
        'parameters': [
            {
                'in': 'query',
                'name': 'atleta',
                'required': False,
                'schema': {'type': 'string'},
            },
            {
                'in': 'query',
                'name': 'posicao',
                'required': False,
                'schema': {'type': 'string'},
            },
            {
                'in': 'query',
                'name': 'clube',
                'required': False,
                'schema': {'type': 'string'},
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
    },
)
router.add_api_route(
    '/atleta/{id}',
    endpoint=atleta_detail,
    tags=['Atleta'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            }
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 1,
                            'type': 'Atleta',
                            'data': {
                                'count': 1,
                                'type': 'Atleta',
                                'data': {
                                    'count': 1,
                                    'type': 'Atleta',
                                    'data': {
                                        'count': 1,
                                        'type': 'Atleta',
                                        'data': {
                                            'nome': 'Igor Cruz',
                                            'data_nascimento': '1985-03-11',
                                            'posicao_primaria': 'atacante',
                                            'posicao_secundaria': 'lateral',
                                            'posicao_terciaria': 'null',
                                            'clube_atual': 'Outro clube novo',
                                            'contratos': [
                                                {
                                                    'tipo': 'Profissional',
                                                    'data_inicio': '2024-02-17',
                                                    'data_termino': '2024-08-17',
                                                    'data_expiracao': '2024-02-19',
                                                },
                                                {
                                                    'tipo': 'Agenciamento',
                                                    'data_inicio': '2024-02-17',
                                                    'data_termino': '2024-08-17',
                                                    'data_expiracao': '2024-02-19',
                                                },
                                                {
                                                    'tipo': 'Imagem',
                                                    'data_inicio': '2024-01-01',
                                                    'data_termino': '2024-12-31',
                                                    'data_expiracao': '2024-07-04',
                                                },
                                            ],
                                            'blob_url': 'https://idexdocsblob.blob.core.windows.net/atleta_1.jpeg',
                                        },
                                    },
                                },
                            },
                        }
                    }
                },
            },
            '404': {
                'description': 'Not found',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'NotFound',
                                    'message': 'Atleta não encontrado',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/questionario/relacionamento/atleta/{id}',
    endpoint=relacionamento,
    tags=['Relacionamento'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 2,
                            'type': 'Relacionamento',
                            'data': [
                                {
                                    'atleta_id': 1,
                                    'receptividade_contrato': 5,
                                    'satisfacao_empresa': 1,
                                    'satisfacao_clube': 2,
                                    'relacao_familiares': 3,
                                    'influencias_externas': 4,
                                    'pendencia_empresa': False,
                                    'pendencia_clube': True,
                                    'data_avaliacao': '2024-05-01',
                                },
                                {
                                    'atleta_id': 1,
                                    'receptividade_contrato': 5,
                                    'satisfacao_empresa': 2,
                                    'satisfacao_clube': 4,
                                    'relacao_familiares': 5,
                                    'influencias_externas': 5,
                                    'pendencia_empresa': False,
                                    'pendencia_clube': False,
                                    'data_avaliacao': '2024-06-05',
                                },
                            ],
                        }
                    }
                },
            },
            '404': {
                'description': 'Not found',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'NotFound',
                                    'message': 'O Atleta não possui questionários cadastrados',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/competicao/atleta/{id}',
    endpoint=competicao,
    tags=['Competição'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 2,
                            'type': 'Relacionamento',
                            'data': {
                                'count': 2,
                                'type': 'Relacionamento',
                                'data': [
                                    {
                                        'nome': 'Competição 1',
                                        'data_competicao': '2022-03-01',
                                        'jogos_completos': 5,
                                        'jogos_parciais': 2,
                                        'minutagem': 320,
                                        'gols': 8,
                                        'assistencias': 1,
                                    },
                                    {
                                        'nome': 'Competição 2',
                                        'data_competicao': '2022-04-01',
                                        'jogos_completos': 7,
                                        'jogos_parciais': 4,
                                        'minutagem': 375,
                                        'gols': 8,
                                        'assistencias': 0,
                                    },
                                ],
                            },
                        }
                    }
                },
            },
            '404': {
                'description': 'Not found',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'NotFound',
                                    'message': 'O Atleta não possui competições cadastradas',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/lesao/atleta/{id}',
    endpoint=lesao,
    tags=['Lesão'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 1,
                            'total': 1,
                            'type': 'Lesão',
                            'data': [
                                {
                                    'data_lesao': '2021-05-11',
                                    'descricao': 'Estiramento do coxa direita',
                                    'data_retorno': '2024-05-11',
                                }
                            ],
                        }
                    }
                },
            },
            '404': {
                'description': 'Not found',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'NotFound',
                                    'message': 'O Atleta não possui controles cadastrados',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)

router.add_api_route(
    '/questionario/relacionamento/create',
    endpoint=relacionamento_create,
    tags=['Relacionamento'],
    methods=['POST'],
    response_model=RelacionamentoResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': RelacionamentoCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de questinário de relacionamento',
                            'description': 'Valores de inteiros devem ser entre 0 e 5',
                            'value': {
                                'atleta_id': 10,
                                'receptividade_contrato': 5,
                                'satisfacao_empresa': 3,
                                'satisfacao_clube': 4,
                                'relacao_familiares': 5,
                                'influencias_externas': 2,
                                'pendencia_empresa': True,
                                'pendencia_clube': True,
                                'data_avaliacao': '2024-01-01',
                            },
                        }
                    },
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/clube/atleta/{id}',
    endpoint=clube,
    tags=['Clube'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 2,
                            'type': 'Clubes',
                            'data': [
                                {
                                    'nome': 'Clube A',
                                    'data_inicio': '2023-01-01',
                                    'data_fim': '2023-01-01',
                                },
                                {
                                    'nome': 'Clube B',
                                    'data_inicio': '2023-01-01',
                                    'data_fim': None,
                                },
                            ],
                        }
                    }
                },
            },
            '404': {
                'description': 'Not found',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'NotFound',
                                    'message': 'O Atleta não possui controles cadastrados',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/create/controle',
    endpoint=controle_create,
    tags=['Controle'],
    methods=['POST'],
    response_model=ControleCreateResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': ControleCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de controle',
                            'description': 'Valores de preço deve ser no formato 300.00',
                            'value': {
                                'atleta_id': 10,
                                'nome': 'Chuteira',
                                'quantidade': 2,
                                'preco': 499.00,
                                'data_controle': '2024-01-01',
                            },
                        }
                    },
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/controle/atleta/{id}',
    endpoint=controle,
    tags=['Controle'],
    methods=['GET'],
    response_model=ControleListResponse,
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 5,
                            'total': 5,
                            'type': 'Controle',
                            'data': {
                                'controles': [
                                    {
                                        'atleta_id': 1,
                                        'nome': 'Uniforme',
                                        'quantidade': 2,
                                        'preco': 50.0,
                                        'data_controle': '2024-01-01',
                                    },
                                    {
                                        'atleta_id': 2,
                                        'nome': 'Uniforme',
                                        'quantidade': 2,
                                        'preco': 50.0,
                                        'data_controle': '2024-01-01',
                                    },
                                    {
                                        'atleta_id': 3,
                                        'nome': 'Uniforme',
                                        'quantidade': 2,
                                        'preco': 50.0,
                                        'data_controle': '2024-01-01',
                                    },
                                    {
                                        'atleta_id': 4,
                                        'nome': 'Uniforme',
                                        'quantidade': 2,
                                        'preco': 50.1,
                                        'data_controle': '2024-01-01',
                                    },
                                    {
                                        'atleta_id': 5,
                                        'nome': 'Uniforme',
                                        'quantidade': 2,
                                        'preco': 50.75,
                                        'data_controle': '2024-01-01',
                                    },
                                ],
                                'total': 250.85,
                            },
                        }
                    }
                },
            },
            '404': {
                'description': 'Not found',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'NotFound',
                                    'message': 'O Atleta não possui controles cadastrados',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/create/clube',
    endpoint=clube_create,
    tags=['Clube'],
    methods=['POST'],
    response_model=ClubeCreateResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': ClubeCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de clube atual',
                            'description': 'Caso seja o clube atual a data fim pertencerá ao clube anterior',
                            'value': {
                                'atleta_id': 1,
                                'nome': 'Clube novo',
                                'data_inicio': '2024-01-01',
                                'clube_atual': True,
                                'data_fim': 'null',
                            },
                        },
                        'example2': {
                            'summary': 'Exemplo de payload para adição de clube ao histórico',
                            'description': 'Caso seja não seja o clube atual a data fim pertencerá ao clube adicionado',
                            'value': {
                                'atleta_id': 1,
                                'nome': 'Clube antigo',
                                'data_inicio': '2024-01-01',
                                'clube_atual': False,
                                'data_fim': '2024-06-01',
                            },
                        },
                    },
                }
            },
            'required': True,
        },
        'responses': {
            '409': {
                'description': 'Conflict',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'Conflict',
                                    'message': 'O atleta já possui clube ativo',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/create/lesao',
    endpoint=lesao_create,
    tags=['Lesão'],
    methods=['POST'],
    response_model=LesaoCreateResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': LesaoCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de clube',
                            'description': 'Caso seja o clube atual não insesir data_fim',
                            'value': {
                                'atleta_id': 1,
                                'descricao': 'Entorse de tornozelo esquerdo',
                                'data_lesao': '2024-01-01',
                            },
                        }
                    },
                }
            },
            'required': True,
        },
        'responses': {
            '409': {
                'description': 'Conflict',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'Conflict',
                                    'message': 'O atleta já possui clube ativo',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/create/competicao',
    endpoint=competicao_create,
    tags=['Competição'],
    methods=['POST'],
    response_model=CompeticaoCreateResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': CompeticaoCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de competição',
                            'value': {
                                'atleta_id': 1,
                                'nome': 'Brasileiro 2023',
                                'data_competicao': '2023-06-13',
                                'jogos_completos': 5,
                                'jogos_parciais': 1,
                                'minutagem': 480,
                                'gols': 12,
                                'assistencias': 2,
                            },
                        }
                    },
                }
            },
            'required': True,
        },
        'responses': {
            '409': {
                'description': 'Conflict',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'Conflict',
                                    'message': 'O atleta já possui clube ativo',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/create/observacao',
    endpoint=observacao_create,
    tags=['Observação'],
    methods=['POST'],
    response_model=ObservacaoCreateResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': ObservacaoCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de observação',
                            'value': {
                                'atleta_id': 2,
                                'tipo': 'relacionamento',
                                'descricao': 'sua obervação',
                            },
                        }
                    },
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/observacao/atleta/{id}',
    endpoint=observacao,
    tags=['Observação'],
    methods=['GET'],
    response_model=ObservacaoListResponse,
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            },
            {
                'in': 'query',
                'name': 'tipo',
                'required': False,
                'schema': {'type': 'string'},
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example1': {
                            'type': 'Observacao',
                            'data': {
                                'id': 5,
                                'tipo': 'relacionamento',
                                'descricao': 'Minha primeira observação',
                                'data_criacao': '2024-05-07',
                            },
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/caracteristica/atleta/{id}/',
    endpoint=caracteristica,
    tags=['Característica'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            },
            {
                'name': 'model',
                'in': 'query',
                'required': True,
                'description': 'Parâmetro de característica do atleta',
                'schema': {
                    'type': 'string',
                    'example': 'fisico, atacante, zagueiro, ...',
                },
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'type': 'CaracteristicaAtacante',
                            'data': {
                                'fisico': [
                                    {
                                        'estatura_fis': 3,
                                        'velocidade_fis': 3,
                                        'um_contra_um_ofensivo_fis': 3,
                                        'desmarques_fis': 3,
                                        'controle_bola_fis': 3,
                                        'cruzamentos_fis': 3,
                                        'finalizacao_fis': 3,
                                        'data_avaliacao': '2024-01-01',
                                        'sum': 21,
                                        'mean': 3.0,
                                    },
                                    {
                                        'estatura_fis': 3,
                                        'velocidade_fis': 3,
                                        'um_contra_um_ofensivo_fis': 3,
                                        'desmarques_fis': 3,
                                        'controle_bola_fis': 3,
                                        'cruzamentos_fis': 3,
                                        'finalizacao_fis': 3,
                                        'data_avaliacao': '2024-02-01',
                                        'sum': 21,
                                        'mean': 3.0,
                                    },
                                ],
                                'tecnico': [
                                    {
                                        'visao_espacial_tec': 3,
                                        'dominio_orientado_tec': 3,
                                        'dribles_em_diagonal_tec': 3,
                                        'leitura_jogo_tec': 3,
                                        'reacao_pos_perda_tec': 3,
                                        'data_avaliacao': '2024-01-01',
                                        'sum': 15,
                                        'mean': 3.0,
                                    },
                                    {
                                        'visao_espacial_tec': 3,
                                        'dominio_orientado_tec': 3,
                                        'dribles_em_diagonal_tec': 3,
                                        'leitura_jogo_tec': 3,
                                        'reacao_pos_perda_tec': 3,
                                        'data_avaliacao': '2024-02-01',
                                        'sum': 15,
                                        'mean': 3.0,
                                    },
                                ],
                                'psicologico': [
                                    {
                                        'criatividade_psi': 3,
                                        'capacidade_decisao_psi': 3,
                                        'inteligencia_tatica_psi': 3,
                                        'competitividade_psi': 3,
                                        'data_avaliacao': '2024-01-01',
                                        'sum': 12,
                                        'mean': 3.0,
                                    },
                                    {
                                        'criatividade_psi': 3,
                                        'capacidade_decisao_psi': 3,
                                        'inteligencia_tatica_psi': 3,
                                        'competitividade_psi': 3,
                                        'data_avaliacao': '2024-02-01',
                                        'sum': 12,
                                        'mean': 3.0,
                                    },
                                ],
                                'total_mean': {
                                    '2024-01-01': 3.0,
                                    '2024-02-01': 3.0,
                                },
                            },
                        }
                    }
                },
            },
            '404': {
                'description': 'Not found',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'NotFound',
                                    'message': 'O Atleta não possui características cadastrados',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/create/caracteristica',
    endpoint=caracteristica_create,
    tags=['Característica'],
    methods=['POST'],
    response_model=CaracteristicaCreateResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de características físicas',
                            'value': {
                                'caracteristica': 'fisico',
                                'atleta_id': 2,
                                'estatura': 170.0,
                                'envergadura': 183.0,
                                'peso': 90.0,
                                'percentual_gordura': 15.3,
                                'data_avaliacao': '2024-01-01',
                            },
                        },
                        'example2': {
                            'summary': 'Exemplo de payload para criação de características para zagueiro',
                            'value': {
                                'caracteristica': 'zagueiro',
                                'atleta_id': 2,
                                'estatura_fis': 3,
                                'força_fis': 3,
                                'passe_curto_fis': 3,
                                'passe_longo_fis': 3,
                                'jogo_aereo_fis': 3,
                                'confronto_defensivo_fis': 3,
                                'leitura_jogo_tec': 3,
                                'ambidestria_tec': 3,
                                'participacao_ofensica_tec': 3,
                                'cabeceio_ofensivo_tec': 3,
                                'passe_entre_linhas_tec': 3,
                                'lideranca_psi': 3,
                                'confianca_psi': 3,
                                'inteligencia_tatica_psi': 3,
                                'competitividade_psi': 3,
                                'data_avaliacao': '2024-01-01',
                            },
                        },
                        'example3': {
                            'summary': 'Exemplo de payload para criação de características para lateral',
                            'value': {
                                'caracteristica': 'lateral',
                                'atleta_id': 2,
                                'estatura_fis': 3,
                                'velocidade_fis': 3,
                                'passe_curto_fis': 3,
                                'passe_longo_fis': 3,
                                'capacidade_aerobia_fis': 3,
                                'fechemanento_defensivo_fis': 3,
                                'leitura_jogo_tec': 3,
                                'participacao_ofensiva_tec': 3,
                                'cruzamento_tec': 3,
                                'jogo_aereo_tec': 3,
                                'conducao_bola_tec': 3,
                                'lideranca_psi': 3,
                                'confianca_psi': 3,
                                'inteligencia_tatica_psi': 3,
                                'competitividade_psi': 3,
                                'data_avaliacao': '2024-01-01',
                            },
                        },
                        'example4': {
                            'summary': 'Exemplo de payload para criação de características para goleiro',
                            'value': {
                                'caracteristica': 'goleiro',
                                'atleta_id': 2,
                                'perfil_fis': 3,
                                'maturacao_fis': 3,
                                'agilidade_fis': 3,
                                'velocidade_membros_superiores_fis': 3,
                                'flexibilidade_fis': 3,
                                'posicionamento_fis': 3,
                                'leitura_jogo_tec': 3,
                                'jogo_com_pes_tec': 3,
                                'organizacao_da_defesa_tec': 3,
                                'dominio_coberturas_e_saidas_tec': 3,
                                'lideranca_psi': 3,
                                'coragem_psi': 3,
                                'concentracao_psi': 3,
                                'controle_estresse_psi': 3,
                                'data_avaliacao': '2024-01-01',
                            },
                        },
                        'example5': {
                            'summary': 'Exemplo de payload para criação de características para volante',
                            'value': {
                                'caracteristica': 'volante',
                                'atleta_id': 2,
                                'estatura_fis': 3,
                                'forca_fis': 3,
                                'passe_curto_fis': 3,
                                'capacidade_aerobia_fis': 3,
                                'dinamica_fis': 3,
                                'visao_espacial_fis': 3,
                                'leitura_jogo_tec': 3,
                                'dominio_orientado_tec': 3,
                                'jogo_aereo_ofensivo_tec': 3,
                                'passes_verticais_tec': 3,
                                'finalizacao_media_distancia_tec': 3,
                                'lideranca_psi': 3,
                                'confianca_psi': 3,
                                'inteligencia_tatica_psi': 3,
                                'competitividade_psi': 3,
                                'data_avaliacao': '2024-01-01',
                            },
                        },
                        'example6': {
                            'summary': 'Exemplo de payload para criação de características para atacante',
                            'value': {
                                'caracteristica': 'atacante',
                                'atleta_id': 2,
                                'estatura_fis': 3,
                                'velocidade_fis': 3,
                                'um_contra_um_ofensivo_fis': 3,
                                'desmarques_fis': 3,
                                'controle_bola_fis': 3,
                                'cruzamentos_fis': 3,
                                'finalizacao_fis': 3,
                                'visao_espacial_tec': 3,
                                'dominio_orientado_tec': 3,
                                'dribles_em_diagonal_tec': 3,
                                'leitura_jogo_tec': 3,
                                'reacao_pos_perda_tec': 3,
                                'criatividade_psi': 3,
                                'capacidade_decisao_psi': 3,
                                'inteligencia_tatica_psi': 3,
                                'competitividade_psi': 3,
                                'data_avaliacao': '2024-01-01',
                            },
                        },
                        'example7': {
                            'summary': 'Exemplo de payload para criação de características para meia',
                            'value': {
                                'caracteristica': 'meia',
                                'atleta_id': 2,
                                'estatura_fis': 3,
                                'velocidade_fis': 3,
                                'leitura_jogo_fis': 3,
                                'desmarques_fis': 3,
                                'controle_bola_fis': 3,
                                'capacidade_aerobia_fis': 3,
                                'finalizacao_fis': 3,
                                'visao_espacial_tec': 3,
                                'dominio_orientado_tec': 3,
                                'dribles_tec': 3,
                                'organizacao_acao_ofensica_tec': 3,
                                'pisada_na_area_para_finalizar_tec': 3,
                                'criatividade_psi': 3,
                                'capacidade_decisao_psi': 3,
                                'confianca_psi': 3,
                                'inteligencia_tatica_psi': 3,
                                'competitividade_psi': 3,
                                'data_avaliacao': '2024-01-01',
                            },
                        },
                    },
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/file-upload/atleta/{id}',
    endpoint=file_upload,
    tags=['File'],
    methods=['POST'],
    openapi_extra={
        'requestBody': {
            'content': {
                'multipart/form-data': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'file': {
                                'type': 'string',
                                'format': 'binary',
                                'description': 'Upload an image file. Supported formats: .png, .jpeg',
                            }
                        },
                    }
                }
            }
        }
    },
)
router.add_api_route(
    '/imagem/update',
    endpoint=imagem_update,
    tags=['File'],
    methods=['PUT'],
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': FileUpdateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para edição de imagem do atleta',
                            'value': {
                                'imagem_id': 30,
                                'descricao': 'Nova descricao para a foto',
                            },
                        }
                    },
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/imagem/delete/{id}',
    endpoint=file_delete,
    tags=['File'],
    methods=['DELETE'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único da imagem',
                'schema': {'type': 'integer', 'example': 1},
            }
        ],
    },
)
router.add_api_route(
    '/multiple-files-upload/atleta/{id}',
    endpoint=multiple_files_upload,
    tags=['File'],
    methods=['POST'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            }
        ],
        'requestBody': {
            'content': {
                'multipart/form-data': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'files': {
                                'type': 'array',
                                'items': {
                                    'type': 'string',
                                    'format': 'binary',
                                },
                                'description': 'Array of image files. Supported formats: .png, .jpeg',
                            }
                        },
                    }
                }
            }
        },
    },
)
router.add_api_route(
    '/avatar/atleta/{id}',
    endpoint=file_download,
    tags=['Avatar'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            }
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'status': True,
                            'blob_url': 'https://idexdocsblob.blob.core.windows.net/atleta_1.jpeg',
                        }
                    }
                },
            },
            '400': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {'status': False, 'blob_url': 'null'},
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/multiple-files-download/atleta/{id}',
    endpoint=multiple_files_download,
    tags=['File'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            }
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'status': True,
                            'blob_url': 'https://idexdocsblob.blob.core.windows.net/atleta_1.jpeg',
                        }
                    }
                },
            },
            '400': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {'status': False, 'blob_url': 'null'},
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/video-upload/atleta/{id}',
    endpoint=video_upload,
    tags=['Video'],
    methods=['POST'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            }
        ],
        'requestBody': {
            'content': {
                'multipart/form-data': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'file': {
                                'type': 'string',
                                'format': 'binary',
                                'description': 'Upload an video file or url. Supported video formats: .mp4, .mov',
                            }
                        },
                    },
                },
                'application/json': {
                    'schema': VideoCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de vídeo',
                            'value': {
                                'video_url': 'url do vídeo do youtube',
                            },
                        }
                    },
                },
            }
        }
    },
)
router.add_api_route(
    '/video-list/atleta/{id}',
    endpoint=video_list,
    tags=['Video'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            }
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 4,
                            'total': 4,
                            'type': 'AtletaVideos',
                            'data': [
                                {
                                    'id': 1,
                                    'blob_url': 'https://idexdocsblob.blob.core.windows.net/atleta-videos/atleta_1/7d78d8c7-7c98-48ce-9c91-c985a9d91901.mp4',
                                    'tipo': 'video',
                                    'descricao': 'moto',
                                },
                                {
                                    'id': 2,
                                    'blob_url': 'https://www.youtube.com/embed/d9nfk2WI17c',
                                    'tipo': 'youtube',
                                    'descricao': 'null',
                                },
                            ],
                        }
                    }
                },
            },
            '400': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {'status': False, 'blob_url': 'null'},
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/video/update',
    endpoint=video_update,
    tags=['Video'],
    methods=['PUT'],
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': VideoUpdateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para edição de vídeo do atleta',
                            'value': {
                                'video_id': 1,
                                'descricao': 'Nova descricao para o vídeo',
                            },
                        }
                    },
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/video/delete/{id}',
    endpoint=video_delete,
    tags=['Video'],
    methods=['DELETE'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do vídeo',
                'schema': {'type': 'integer', 'example': 1},
            }
        ],
    },
)
router.add_api_route(
    '/create/pdf/atleta/{id}',
    endpoint=pdf_create,
    tags=['PDF'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            },
            {
                'name': 'permissoes',
                'in': 'query',
                'required': False,
                'description': 'Permissão para impressão do pdf',
                'schema': {
                    'type': 'string',
                    'example': ['create_desempenho', 'create_relacionamento'],
                },
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'atleta': {
                                'nome': 'Igor Cruz',
                                'data_nascimento': '1985-03-11',
                                'posicao_primaria': 'atacante',
                                'posicao_secundaria': 'lateral',
                                'posicao_terciaria': 'null',
                                'clube_atual': 'Outro clube novo',
                                'contratos': [
                                    {
                                        'tipo': 'Profissional',
                                        'data_inicio': '2024-01-01',
                                        'data_termino': '2024-01-01',
                                        'data_expiracao': '2023-07-05',
                                    },
                                    {
                                        'tipo': 'Agenciamento',
                                        'data_inicio': '2024-02-17',
                                        'data_termino': '2024-08-17',
                                        'data_expiracao': '2024-02-19',
                                    },
                                    {
                                        'tipo': 'Imagem',
                                        'data_inicio': '2024-01-01',
                                        'data_termino': '2024-12-31',
                                        'data_expiracao': '2024-07-04',
                                    },
                                ],
                                'blob_url': 'https://idexdocsblob.blob.core.windows.net/atleta_1.jpeg',
                                'ativo': True,
                            },
                            'clube': [
                                {
                                    'clube_id': 10,
                                    'nome': 'São João',
                                    'data_inicio': '2024-01-01',
                                    'data_fim': '2025-01-01',
                                },
                                {
                                    'clube_id': 29,
                                    'nome': 'Clube novo',
                                    'data_inicio': '2024-01-01',
                                    'data_fim': '2025-01-01',
                                },
                            ],
                            'lesao': [
                                {
                                    'data_lesao': '2021-05-11',
                                    'descricao': 'Estiramento do coxa direita',
                                },
                                {
                                    'data_lesao': '2021-05-11',
                                    'descricao': 'Estiramento do coxa direita',
                                },
                            ],
                            'controle': [
                                {
                                    'atleta_id': 1,
                                    'nome': 'Uniforme',
                                    'quantidade': 2,
                                    'preco': 50.0,
                                    'data_controle': '2024-01-01',
                                },
                                {
                                    'atleta_id': 2,
                                    'nome': 'Uniforme',
                                    'quantidade': 2,
                                    'preco': 50.0,
                                    'data_controle': '2024-01-01',
                                },
                            ],
                            'competicao': [
                                {
                                    'nome': 'Brasileiro 2023',
                                    'data_competicao': '2023-06-13',
                                    'jogos_completos': 5,
                                    'jogos_parciais': 1,
                                    'minutagem': 480,
                                    'gols': 12,
                                    'assistencias': 1,
                                },
                                {
                                    'nome': 'Brasileiro 2023',
                                    'data_competicao': '2023-06-13',
                                    'jogos_completos': 5,
                                    'jogos_parciais': 1,
                                    'minutagem': 480,
                                    'gols': 12,
                                    'assistencias': 1,
                                },
                            ],
                            'observacoes_relacionamento': {
                                'id': 5,
                                'tipo': 'relacionamento',
                                'descricao': 'Minha primeira observação',
                                'data_criacao': '2024-05-07',
                            },
                            'observacoes_desempenho': {
                                'id': 7,
                                'tipo': 'desempenho',
                                'descricao': 'Minha primeira observação',
                                'data_criacao': '2024-05-07',
                            },
                            'relacionamento': [
                                {
                                    'atleta_id': 1,
                                    'receptividade_contrato': 5,
                                    'satisfacao_empresa': 1,
                                    'satisfacao_clube': 2,
                                    'relacao_familiares': 3,
                                    'influencias_externas': 4,
                                    'pendencia_empresa': False,
                                    'pendencia_clube': True,
                                    'data_avaliacao': '2024-01-01',
                                },
                                {
                                    'atleta_id': 1,
                                    'receptividade_contrato': 5,
                                    'satisfacao_empresa': 1,
                                    'satisfacao_clube': 2,
                                    'relacao_familiares': 3,
                                    'influencias_externas': 4,
                                    'pendencia_empresa': False,
                                    'pendencia_clube': True,
                                    'data_avaliacao': '2024-01-01',
                                },
                            ],
                            'caracteristicas_fisicas': [
                                {
                                    'id': 1,
                                    'estatura': 177.0,
                                    'envergadura': 183.0,
                                    'peso': 92.0,
                                    'percentual_gordura': 17.0,
                                    'data_avaliacao': '2024-01-01',
                                    'data_criacao': '2024-05-03 04:02:54',
                                    'data_atualizado': 'null',
                                    'atleta_id': 1,
                                },
                                {
                                    'id': 1002,
                                    'estatura': 170.0,
                                    'envergadura': 180.0,
                                    'peso': 90.0,
                                    'percentual_gordura': 10.0,
                                    'data_avaliacao': '2024-01-01',
                                    'data_criacao': '2024-05-03 13:24:10',
                                    'data_atualizado': 'null',
                                    'atleta_id': 1,
                                },
                            ],
                            'caracteristicas_posicao': {
                                'fisico': [
                                    {
                                        'estatura_fis': 3,
                                        'velocidade_fis': 3,
                                        'um_contra_um_ofensivo_fis': 3,
                                        'desmarques_fis': 3,
                                        'controle_bola_fis': 3,
                                        'cruzamentos_fis': 3,
                                        'finalizacao_fis': 3,
                                        'data_avaliacao': '2024-01-01',
                                        'sum': 21,
                                        'mean': 3.0,
                                    },
                                    {
                                        'estatura_fis': 3,
                                        'velocidade_fis': 3,
                                        'um_contra_um_ofensivo_fis': 3,
                                        'desmarques_fis': 3,
                                        'controle_bola_fis': 3,
                                        'cruzamentos_fis': 3,
                                        'finalizacao_fis': 3,
                                        'data_avaliacao': '2024-02-01',
                                        'sum': 21,
                                        'mean': 3.0,
                                    },
                                ],
                                'tecnico': [
                                    {
                                        'visao_espacial_tec': 3,
                                        'dominio_orientado_tec': 3,
                                        'dribles_em_diagonal_tec': 3,
                                        'leitura_jogo_tec': 3,
                                        'reacao_pos_perda_tec': 3,
                                        'data_avaliacao': '2024-01-01',
                                        'sum': 15,
                                        'mean': 3.0,
                                    },
                                    {
                                        'visao_espacial_tec': 3,
                                        'dominio_orientado_tec': 3,
                                        'dribles_em_diagonal_tec': 3,
                                        'leitura_jogo_tec': 3,
                                        'reacao_pos_perda_tec': 3,
                                        'data_avaliacao': '2024-02-01',
                                        'sum': 15,
                                        'mean': 3.0,
                                    },
                                ],
                                'psicologico': [
                                    {
                                        'criatividade_psi': 3,
                                        'capacidade_decisao_psi': 3,
                                        'inteligencia_tatica_psi': 3,
                                        'competitividade_psi': 3,
                                        'data_avaliacao': '2024-01-01',
                                        'sum': 12,
                                        'mean': 3.0,
                                    },
                                    {
                                        'criatividade_psi': 3,
                                        'capacidade_decisao_psi': 3,
                                        'inteligencia_tatica_psi': 3,
                                        'competitividade_psi': 3,
                                        'data_avaliacao': '2024-02-01',
                                        'sum': 12,
                                        'mean': 3.0,
                                    },
                                ],
                                'total_mean': {
                                    '2024-01-01': 3.0,
                                    '2024-02-01': 3.0,
                                },
                            },
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/usuarios',
    endpoint=usuario_list,
    tags=['Usuário'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 1,
                            'total': 1,
                            'type': 'Usuarios',
                            'data': [
                                {
                                    'nome': 'Igor de Freitas Cruz',
                                    'email': 'igor.freitas.cruz@icloud.com',
                                    'data_criacao': '2024-05-07',
                                    'tipo': 'admin',
                                }
                            ],
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/create/contrato',
    endpoint=contrato_create,
    tags=['Contrato'],
    methods=['POST'],
    response_model=ContratoCreateResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': ContratoCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de contrato',
                            'value': {
                                'atleta_id': 1,
                                'contrato_sub_tipo_id': 2,
                                'data_inicio': '2024-01-01',
                                'data_termino': '2024-02-31',
                                'observacao': 'null',
                            },
                        }
                    },
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/update/contrato',
    endpoint=contrato_update,
    tags=['Contrato'],
    methods=['PUT'],
    response_model=ContratoCreateResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': ContratoUpdateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para edição de contrato',
                            'value': {
                                'atleta_id': 1,
                                'contrato_sub_tipo_id': 1,
                                'data_inicio': '2024-01-01',
                                'data_termino': '2024-01-01',
                                'observacao': 'Alterações contratuais',
                            },
                        }
                    },
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/contrato',
    endpoint=contrato_tipo_list,
    tags=['Contrato'],
    methods=['GET'],
    response_model=ContratoTipoResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'examples': {
                        'example1': {
                            'type': 'ContratoTipo',
                            'data': {
                                'contrato_tipos': [
                                    {
                                        'id': 1,
                                        'tipo': 'Empresa',
                                        'contrato_sub_tipos': [
                                            {'id': 1, 'nome': 'Imagem'},
                                            {'id': 2, 'nome': 'Agenciamento'},
                                            {'id': 6, 'nome': 'Garantias'},
                                            {
                                                'id': 7,
                                                'nome': 'Material esportivo',
                                            },
                                            {'id': 8, 'nome': 'Publicidade'},
                                        ],
                                    },
                                    {
                                        'id': 2,
                                        'tipo': 'Clube',
                                        'contrato_sub_tipos': [
                                            {'id': 3, 'nome': 'Profissional'},
                                            {'id': 4, 'nome': 'Amador'},
                                            {'id': 5, 'nome': 'Formação'},
                                        ],
                                    },
                                ]
                            },
                        }
                    },
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/contrato/atleta/{id}',
    endpoint=contrato_list,
    tags=['Contrato'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'in': 'path',
                'name': 'id',
                'required': True,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 3,
                            'total': 3,
                            'type': 'Contratos',
                            'data': [
                                {
                                    'contrato_id': 1004,
                                    'contrato_tipo': 'Clube',
                                    'contrato_nome': 'Profissional',
                                    'versao': 6,
                                    'observacao': 'Alterações contratuais',
                                    'data_inicio': '2024-01-01',
                                    'data_termino': '2024-01-01',
                                    'ativo': True,
                                },
                                {
                                    'contrato_id': 1005,
                                    'contrato_tipo': 'Empresa',
                                    'contrato_nome': 'Agenciamento',
                                    'versao': 1,
                                    'observacao': 'null',
                                    'data_inicio': '2024-02-17',
                                    'data_termino': '2024-08-17',
                                    'ativo': True,
                                },
                                {
                                    'contrato_id': 1008,
                                    'contrato_tipo': 'Empresa',
                                    'contrato_nome': 'Imagem',
                                    'versao': 1,
                                    'observacao': 'null',
                                    'data_inicio': '2024-01-01',
                                    'data_termino': '2024-12-31',
                                    'ativo': True,
                                },
                            ],
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/contrato/versao/{id}',
    endpoint=contrato_versao_list,
    tags=['Contrato'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'in': 'path',
                'name': 'id',
                'required': True,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 2,
                            'total': 2,
                            'type': 'Contratos',
                            'data': [
                                {
                                    'contrato_id': 1,
                                    'contrato_tipo': 'Clube',
                                    'contrato_nome': 'Profissional',
                                    'data_inicio': '2024-02-16',
                                    'data_termino': '2024-08-16',
                                    'observacao': 'null',
                                    'ativo': True,
                                },
                                {
                                    'contrato_id': 2,
                                    'contrato_tipo': 'Empresa',
                                    'contrato_nome': 'Agenciamento',
                                    'data_inicio': '2024-02-16',
                                    'data_termino': '2024-08-16',
                                    'observacao': 'Recisão de contrato',
                                    'ativo': False,
                                },
                            ],
                        }
                    }
                },
            },
        },
    },
)


def init_app(app):
    app.include_router(router)
