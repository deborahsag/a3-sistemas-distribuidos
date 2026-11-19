from pydantic import BaseModel

class IdeiaBase(BaseModel):
    titulo: str | None = 'Nova Ideia'
    descricao: str
    notificacao: int = 0

class IdeiaResponse(IdeiaBase):
    id: str
    timestamp: str
    arquivado: bool
    projetoId: str | None = None
