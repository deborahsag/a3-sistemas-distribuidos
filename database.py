import firebase_admin
from firebase_admin import firestore, credentials
from datetime import datetime, timezone

# Chave privada de acesso ao Firebase Firestore
CHAVE_PRIVADA = "./chave-privada/a3-202602-capsula-firebase-adminsdk-fbsvc-5dac698542.json"

# Inicializar Firebase Admin SDK
def inicializar_banco():
    cred = credentials.Certificate(CHAVE_PRIVADA)
    firebase_admin.initialize_app(cred)

def conectar_banco():
    db = firestore.client()
    return db


# Criação de registros
def registrar_ideia(ideia: dict):
    db = conectar_banco()
    timestamp = datetime.now(timezone.utc).isoformat()
    arquivada = False
    doc_ref = db.collection('Ideias').add({**ideia, "timestamp": timestamp, "arquivada": arquivada})
    return doc_ref[1].id, timestamp, arquivada


# Consulta de registros
def listar_ideias():
    db = conectar_banco()
    ideias_ref = db.collection('Ideias')
    docs =  ideias_ref.stream()
    ideias = [{**doc.to_dict(), 'id': doc.id} for doc in docs]
    return ideias

def buscar_ideia(ideia_id: str):
    db = conectar_banco()
    doc = db.collection('Ideias').document(ideia_id).get()
    if doc.exists:
        return {**doc.to_dict(), 'id': doc.id}
    else:
        return None


# Modificação de registros
def modificar_ideia(ideia_id: str, atualizacao: dict):
    db = conectar_banco()
    doc_ref = db.collection('Ideias').document(ideia_id)
    dados_atualizacao = atualizacao
    doc_ref.update(dados_atualizacao)
    ideia_atualizada = doc_ref.get().to_dict()
    return {**ideia_atualizada, 'id': ideia_id}


# Exclusão de registros
def excluir_ideia(ideia_id: str):
    db = conectar_banco()
    doc_ref = db.collection('Ideias').document(ideia_id)
    doc_ref.delete()
