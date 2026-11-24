from ..schemas.projeto import ProjetoBase, ProjetoResponse
from ..database.database import *

def criar_projeto(projeto: ProjetoBase):
    ideia_original = buscar_registro_por_id("ideias", projeto.ideiaOriginalId)
    dados_projeto = {
        **projeto.model_dump(),
        "ideiaOriginalTitulo": ideia_original["titulo"],
        "ideiaOriginalDescricao": ideia_original["descricao"],
        "ideiaOriginalTimestamp": ideia_original["timestamp"],
    }

    novo_id, timestamp, arquivado = criar_registro("projetos", dados_projeto)

    atualizacao = {"projetoId": novo_id}
    ideia_atualizada = modificar_registro("ideias", projeto.ideiaOriginalId, atualizacao)

    projeto_novo = {
        **dados_projeto,
        "id": novo_id,
        "timestamp": timestamp,
        "arquivado": arquivado,
    }
    return ProjetoResponse(**projeto_novo)

def listar_projetos():
    dict_projetos = listar_registros("projetos")
    projetos = [ProjetoResponse(**projeto) for projeto in dict_projetos]
    return projetos

def buscar_projeto_por_id(projeto_id: str):
    dict_projeto = buscar_registro_por_id("projetos", projeto_id)
    if not dict_projeto:
        return None
    return ProjetoResponse(**dict_projeto)