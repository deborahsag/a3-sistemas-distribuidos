from fastapi import APIRouter, HTTPException

from ..services.projetos import *

router = APIRouter(
    prefix="/projetos",
    tags=["projetos"],
)

@router.post("/", response_model=ProjetoResponse, status_code=201)
def criar_novo_projeto(projeto: ProjetoBase):
    # Código 400 (Bad Request) para regra de negócio inválida
    if not projeto.ideiaOriginalId.strip():
        raise HTTPException(status_code=400, detail="O projeto deve ter uma Ideia Original.")
    try:
        return criar_projeto(projeto)
    except Exception as e:
        # Código 500 (Internal Server Error)
        raise HTTPException(status_code=500, detail=f"Erro interno no banco de dados: {str(e)}")

@router.get("/", response_model=list[ProjetoResponse], status_code=200)
def consultar_projetos():
    return listar_projetos()

@router.get("/{projeto_id}", response_model=ProjetoResponse, status_code=200)
def consultar_projeto_por_id(projeto_id: str):
    projeto = buscar_projeto_por_id(projeto_id)
    if not projeto:
        # Código 404 (Not Found)
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    return projeto

@router.put("/{projeto_id}", response_model=ProjetoResponse, status_code=200)
def atualizar_projeto(projeto_id: str, atualizacao: ProjetoEdicao):
    projeto = buscar_projeto_por_id(projeto_id)
    if not projeto:
        # Código 404 (Not Found)
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    try:
        return modificar_projeto(projeto_id, atualizacao)
    except Exception as e:
        # Código 500 (Internal Server Error)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/{projeto_id}", status_code=200)
def deletar_projeto(projeto_id: str):
    projeto = buscar_projeto_por_id(projeto_id)
    if not projeto:
        # Código 404 (Not Found)
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    excluir_projeto(projeto_id)
    return {"mensagem": "Projeto removido com sucesso."}
