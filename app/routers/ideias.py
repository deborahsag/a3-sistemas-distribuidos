from fastapi import APIRouter, HTTPException

from ..database.database import *
from ..schemas.ideia import IdeiaBase, IdeiaResponse, IdeiaEdicao

router = APIRouter(
    prefix='/ideias',
    tags=["ideias"],
)

@router.post("/", response_model=IdeiaResponse, status_code=201)
def criar_nova_ideia(ideia: IdeiaBase):
    # Código 400 (Bad Request) para regra de negócio inválida
    if not ideia.descricao.strip():
        raise HTTPException(status_code=400, detail="A descrição não pode estar em branco.")
    try:
        novo_id, timestamp, arquivado = criar_registro("ideias", ideia.model_dump())
        return {**ideia.model_dump(), "id": novo_id, "timestamp": timestamp, "arquivado": arquivado}
    except Exception as e:
        # Código 500 (Internal Server Error)
        raise HTTPException(status_code=500, detail=f"Erro interno no banco de dados: {str(e)}")


@router.get("/", response_model=list[IdeiaResponse], status_code=200)
def consultar_ideias():
    dict_ideias = listar_registros("ideias")
    ideias = [IdeiaResponse(**ideia) for ideia in dict_ideias]
    return ideias

@router.get("/{ideia_id}", response_model=IdeiaResponse)
def consultar_ideia_por_id(ideia_id: str):
    dict_ideia = buscar_registro_por_id("ideias", ideia_id)
    if not dict_ideia:
        # Código 404 (Not Found)
        raise HTTPException(status_code=404, detail="Ideia não encontrada.")
    ideia = IdeiaResponse(**dict_ideia)
    return ideia


@router.put("/{ideia_id}", response_model=IdeiaResponse, status_code=200)
def atualizar_ideia(ideia_id: str, atualizacao: IdeiaEdicao):
    ideia = buscar_registro_por_id("ideias", ideia_id)
    if not ideia:
        # Código 404 (Not Found)
        raise HTTPException(status_code=404, detail="Ideia não encontrada.")
    try:
        dados_atualizacao = atualizacao.model_dump(exclude_unset=True)
        dict_ideia = modificar_registro("ideias", ideia_id, dados_atualizacao)
        return IdeiaResponse(**dict_ideia)
    except Exception as e:
        # Código 500 (Internal Server Error)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.delete("/{ideia_id}", status_code=200)
def deletar_ideia(ideia_id: str):
    ideia = buscar_registro_por_id("ideias", ideia_id)
    if not ideia:
        # Código 404 (Not Found)
        raise HTTPException(status_code=404, detail="Ideia não encontrada.")
    excluir_registro("ideias", ideia_id)
    return {"mensagem": "Ideia removida com sucesso."}
