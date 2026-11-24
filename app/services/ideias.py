from ..schemas.ideia import IdeiaBase, IdeiaResponse, IdeiaEdicao
from ..database.database import *

def criar_ideia(ideia: IdeiaBase):
    novo_id, timestamp, arquivado = criar_registro("ideias", ideia.model_dump())
    ideia_nova = {**ideia.model_dump(), "id": novo_id, "timestamp": timestamp, "arquivado": arquivado}
    return IdeiaResponse(**ideia_nova)

def listar_ideias():
    dict_ideias = listar_registros("ideias")
    ideias = [IdeiaResponse(**ideia) for ideia in dict_ideias]
    return ideias

def buscar_ideia_por_id(ideia_id: str):
    dict_ideia = buscar_registro_por_id("ideias", ideia_id)
    if not dict_ideia:
        return None
    return IdeiaResponse(**dict_ideia)

def modificar_ideia(ideia_id: str, atualizacao: IdeiaEdicao):
    dados_atualizacao = atualizacao.model_dump(exclude_unset=True)
    dict_ideia = modificar_registro("ideias", ideia_id, dados_atualizacao)
    return IdeiaResponse(**dict_ideia)

def excluir_ideia(ideia_id: str):
    excluir_registro("ideias", ideia_id)
