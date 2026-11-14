import firebase_admin
from firebase_admin import firestore, credentials
from datetime import datetime

from models import IdeiaBase, IdeiaResponse


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
