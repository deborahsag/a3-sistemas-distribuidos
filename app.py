from fastapi import FastAPI, HTTPException

from database import *
from models import *

# Inicializar banco de dados
inicializar_banco()

# Criar instância do FastAPI
app = FastAPI()


@app.post("/ideias", response_model=IdeiaResponse, status_code=201)
def criar_nova_ideia(ideia: IdeiaBase):
    # Código 400 (Bad Request) para regra de negócio inválida
    if not ideia.descricao.strip():
        raise HTTPException(status_code=400, detail="A descrição não pode estar em branco.")
    try:
        novo_id, timestamp, arquivada = registrar_ideia(ideia)
        return {**ideia.model_dump(), "id": novo_id, "timestamp": timestamp, "arquivada": arquivada}
    except Exception as e:
        # Código 500 (Internal Server Error)
        raise HTTPException(status_code=500, detail=f"Erro interno no banco de dados: {str(e)}")


@app.get("/ideias", response_model=list[IdeiaResponse], status_code=200)
def consultar_ideias():
    ideias = listar_ideias()
    return ideias

@app.get("/ideias/{ideia_id}", response_model=IdeiaResponse)
def consultar_ideia_por_id(ideia_id: str):
    ideia = buscar_ideia(ideia_id)
    if not ideia:
        # Código 404 (Not Found)
        raise HTTPException(status_code=404, detail="Ideia não encontrada.")
    return ideia


@app.put("/ideias/{ideia_id}", response_model=IdeiaResponse, status_code=200)
def atualizar_ideia(ideia_id: str, atualizacao: Modificaveis):
    ideia = buscar_ideia(ideia_id)
    if not ideia:
        # Código 404 (Not Found)
        raise HTTPException(status_code=404, detail="Ideia não encontrada.")
    try:
        return modificar_ideia(ideia_id, atualizacao)
    except Exception as e:
        # Código 500 (Internal Server Error)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@app.delete("/ideias/{ideia_id}", status_code=200)
def deletar_ideia(ideia_id: str):
    ideia = buscar_ideia(ideia_id)
    if not ideia:
        # Código 404 (Not Found)
        raise HTTPException(status_code=404, detail="Ideia não encontrada.")
    excluir_ideia(ideia_id)
    return {"mensagem": "Ideia removida com sucesso."}
