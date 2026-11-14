import firebase_admin
from firebase_admin import firestore, credentials
from datetime import datetime

from models import *


# Inicializar Firebase Admin SDK
def inicializar_banco():
    cred = credentials.Certificate(
        "/home/debor/projetos/a3-2026-2/chave-privada/a3-202602-capsula-firebase-adminsdk-fbsvc-5dac698542.json")
    firebase_admin.initialize_app(cred)

def conectar_banco():
    db = firestore.client()
    return db


# Criação de registros
def registrar_ideia(ideia: IdeiaBase):
    db = conectar_banco()
    timestamp = datetime.now().isoformat()
    arquivada = False
    doc_ref = db.collection('Ideias').add({**ideia.model_dump(), "timestamp": timestamp, "arquivada": arquivada})
    return doc_ref[1].id, timestamp, arquivada


# Consulta de registros
def listar_ideias():
    db = conectar_banco()
    ideias_ref = db.collection('Ideias')
    docs =  ideias_ref.stream()
    ideias = [IdeiaResponse(**doc.to_dict(), id=doc.id) for doc in docs]
    return ideias

def buscar_ideia(ideia_id: str):
    db = conectar_banco()
    doc = db.collection('Ideias').document(ideia_id).get()
    if doc.exists:
        return IdeiaResponse(**doc.to_dict(), id=doc.id)
    else:
        return None


# Modificação de registros
def modificar_ideia(ideia_id: str, atualizacao: Modificaveis):
    db = conectar_banco()
    doc_ref = db.collection('Ideias').document(ideia_id)
    dados_atualizacao = atualizacao.model_dump(exclude_unset=True)
    doc_ref.update(dados_atualizacao)
    ideia_atualizada = doc_ref.get().to_dict()
    return IdeiaResponse(**ideia_atualizada, id=ideia_id)


# Exclusão de registros
def excluir_ideia(ideia_id: str):
    db = conectar_banco()
    doc_ref = db.collection('Ideias').document(ideia_id)
    doc_ref.delete()
