from datetime import datetime

from pydantic import BaseModel, field_validator


def validate_date_format(date_str: str) -> str:
    if date_str is not None:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            raise ValueError('Formato de data inválido, utilize YYYY-MM-DD')


class CaracteristicaFisicaCreateSchema(BaseModel):
    caracteristica: str
    estatura: float
    envergadura: float
    peso: float
    percentual_gordura: float
    atleta_id: int
    data_avaliacao: str

    _validate_data_inicio = field_validator('data_avaliacao')(
        validate_date_format
    )


class CaracteristicaZagueiroCreateSchema(BaseModel):
    caracteristica: str
    estatura_fis: int
    força_fis: int
    passe_curto_fis: int
    passe_longo_fis: int
    jogo_aereo_fis: int
    confronto_defensivo_fis: int
    leitura_jogo_tec: int
    ambidestria_tec: int
    participacao_ofensica_tec: int
    cabeceio_ofensivo_tec: int
    passe_entre_linhas_tec: int
    lideranca_psi: int
    confianca_psi: int
    inteligencia_tatica_psi: int
    competitividade_psi: int
    atleta_id: int
    data_avaliacao: str

    _validate_data_inicio = field_validator('data_avaliacao')(
        validate_date_format
    )


class CaracteristicaLateralCreateSchema(BaseModel):
    caracteristica: str
    estatura_fis: int
    velocidade_fis: int
    passe_curto_fis: int
    passe_longo_fis: int
    capacidade_aerobia_fis: int
    fechemanento_defensivo_fis: int
    leitura_jogo_tec: int
    participacao_ofensiva_tec: int
    cruzamento_tec: int
    jogo_aereo_tec: int
    conducao_bola_tec: int
    lideranca_psi: int
    confianca_psi: int
    inteligencia_tatica_psi: int
    competitividade_psi: int
    atleta_id: int
    data_avaliacao: str

    _validate_data_inicio = field_validator('data_avaliacao')(
        validate_date_format
    )


class CaracteristicaGoleiroCreateSchema(BaseModel):
    caracteristica: str
    perfil_fis: int
    maturacao_fis: int
    agilidade_fis: int
    velocidade_membros_superiores_fis: int
    flexibilidade_fis: int
    posicionamento_fis: int
    leitura_jogo_tec: int
    jogo_com_pes_tec: int
    organizacao_da_defesa_tec: int
    dominio_coberturas_e_saidas_tec: int
    lideranca_psi: int
    coragem_psi: int
    concentracao_psi: int
    controle_estresse_psi: int
    atleta_id: int
    data_avaliacao: str

    _validate_data_inicio = field_validator('data_avaliacao')(
        validate_date_format
    )


class CaracteristicaVolanteCreateSchema(BaseModel):
    caracteristica: str
    estatura_fis: int
    forca_fis: int
    passe_curto_fis: int
    capacidade_aerobia_fis: int
    dinamica_fis: int
    visao_espacial_fis: int
    leitura_jogo_tec: int
    dominio_orientado_tec: int
    jogo_aereo_ofensivo_tec: int
    passes_verticais_tec: int
    finalizacao_media_distancia_tec: int
    lideranca_psi: int
    confianca_psi: int
    inteligencia_tatica_psi: int
    competitividade_psi: int
    atleta_id: int
    data_avaliacao: str

    _validate_data_inicio = field_validator('data_avaliacao')(
        validate_date_format
    )


class CaracteristicaAtacanteCreateSchema(BaseModel):
    caracteristica: str
    estatura_fis: int
    velocidade_fis: int
    um_contra_um_ofensivo_fis: int
    desmarques_fis: int
    controle_bola_fis: int
    cruzamentos_fis: int
    finalizacao_fis: int
    visao_espacial_tec: int
    dominio_orientado_tec: int
    dribles_em_diagonal_tec: int
    leitura_jogo_tec: int
    reacao_pos_perda_tec: int
    criatividade_psi: int
    capacidade_decisao_psi: int
    inteligencia_tatica_psi: int
    competitividade_psi: int
    atleta_id: int
    data_avaliacao: str

    _validate_data_inicio = field_validator('data_avaliacao')(
        validate_date_format
    )


class CaracteristicaMeiaCreateSchema(BaseModel):
    caracteristica: str
    estatura_fis: int
    velocidade_fis: int
    leitura_jogo_fis: int
    desmarques_fis: int
    controle_bola_fis: int
    capacidade_aerobia_fis: int
    finalizacao_fis: int
    visao_espacial_tec: int
    dominio_orientado_tec: int
    dribles_tec: int
    organizacao_acao_ofensica_tec: int
    pisada_na_area_para_finalizar_tec: int
    criatividade_psi: int
    capacidade_decisao_psi: int
    confianca_psi: int
    inteligencia_tatica_psi: int
    competitividade_psi: int
    atleta_id: int
    data_avaliacao: str

    _validate_data_inicio = field_validator('data_avaliacao')(
        validate_date_format
    )


class CaracteristicaCreateResponse(BaseModel):
    id: int
