import firebase_admin
from firebase_admin import firestore, credentials

from ..config import settings

from datetime import datetime, timezone

# Inicializar Firebase Admin SDK
def inicializar_banco():
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.firebase_credentials)
        firebase_admin.initialize_app(cred)

def conectar_banco():
    return firestore.client()


# Criação de registros
def criar_registro(tabela: str, registro: dict):
    db = conectar_banco()
    timestamp = datetime.now(timezone.utc).isoformat()
    arquivado = False
    doc_ref = db.collection(tabela).add({**registro, "timestamp": timestamp, "arquivado": arquivado})
    return doc_ref[1].id, timestamp, arquivado


# Consulta de registros
def listar_registros(tabela: str):
    db = conectar_banco()
    doc_ref = db.collection(tabela)
    docs =  doc_ref.order_by('timestamp').stream()
    registros = [{**doc.to_dict(), 'id': doc.id} for doc in docs]
    return registros

def buscar_registro_por_id(tabela: str, registro_id: str):
    db = conectar_banco()
    doc = db.collection(tabela).document(registro_id).get()
    if doc.exists:
        return {**doc.to_dict(), 'id': doc.id}
    else:
        return None


# Modificação de registros
def modificar_registro(tabela: str, registro_id: str, atualizacao: dict):
    db = conectar_banco()
    doc_ref = db.collection(tabela).document(registro_id)
    doc_ref.update(atualizacao)
    registro_atualizado = doc_ref.get().to_dict()
    return {**registro_atualizado, 'id': registro_id}


# Exclusão de registros
def excluir_registro(tabela:str, registro_id: str):
    db = conectar_banco()
    doc_ref = db.collection(tabela).document(registro_id)
    doc_ref.delete()
