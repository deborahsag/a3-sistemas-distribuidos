from fastapi import APIRouter, HTTPException

from app.services.ideias import *

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
        return criar_ideia(ideia)
    except Exception as e:
        # Código 500 (Internal Server Error)
        raise HTTPException(status_code=500, detail=f"Erro interno no banco de dados: {str(e)}")


@router.get("/", response_model=list[IdeiaResponse], status_code=200)
def consultar_ideias():
    return listar_ideias()

@router.get("/{ideia_id}", response_model=IdeiaResponse)
def consultar_ideia_por_id(ideia_id: str):
    ideia = buscar_ideia_por_id(ideia_id)
    if not ideia:
        # Código 404 (Not Found)
        raise HTTPException(status_code=404, detail="Ideia não encontrada.")
    return ideia


@router.put("/{ideia_id}", response_model=IdeiaResponse, status_code=200)
def atualizar_ideia(ideia_id: str, atualizacao: IdeiaEdicao):
    ideia = buscar_ideia_por_id(ideia_id)
    if not ideia:
        # Código 404 (Not Found)
        raise HTTPException(status_code=404, detail="Ideia não encontrada.")
    try:
        return modificar_ideia(ideia_id, atualizacao)
    except Exception as e:
        # Código 500 (Internal Server Error)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.delete("/{ideia_id}", status_code=200)
def deletar_ideia(ideia_id: str):
    ideia = buscar_ideia_por_id(ideia_id)
    if not ideia:
        # Código 404 (Not Found)
        raise HTTPException(status_code=404, detail="Ideia não encontrada.")
    excluir_ideia(ideia_id)
    return {"mensagem": "Ideia removida com sucesso."}
