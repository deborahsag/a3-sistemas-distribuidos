from pydantic import BaseModel

class IdeiaBase(BaseModel):
    titulo: str | None = 'Nova Ideia'
    descricao: str
    notificacao: int | None = None

class IdeiaResponse(IdeiaBase):
    id: str
    timestamp: str
    arquivada: bool
