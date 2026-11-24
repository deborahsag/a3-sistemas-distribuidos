from enum import Enum
from typing import Annotated, Literal
from pydantic import BaseModel, Field

class TipoCampoProjeto(str, Enum):
    texto = 'texto'
    lista = 'lista'

class ChecklistItem(BaseModel):
    isChecked: bool = False
    texto: str

class CampoProjeto(BaseModel):
    tipo: TipoCampoProjeto

class CampoTexto(CampoProjeto):
    tipo: Literal[TipoCampoProjeto.texto] = TipoCampoProjeto.texto
    texto: str

class CampoLista(CampoProjeto):
    tipo: Literal[TipoCampoProjeto.lista] = TipoCampoProjeto.lista
    checklist: list[ChecklistItem]

CampoProjetoUnion = Annotated[
    CampoTexto | CampoLista,
    Field(discriminator='tipo')
]

class ProjetoBase(BaseModel):
    titulo: str | None = 'Novo Projeto'
    ideiaOriginalId: str
    notificacao: int = 0
    camposProjeto: list[CampoProjetoUnion] = Field(default_factory=list)

class ProjetoResponse(ProjetoBase):
    id: str
    timestamp: str
    arquivado: bool
    ideiaOriginalTitulo: str
    ideiaOriginalDescricao: str
    ideiaOriginalTimestamp: str

class ProjetoEdicao(BaseModel):
    titulo: str | None = None
    notificacao: int | None = None
    arquivado: bool | None = None
    camposProjeto: list[CampoProjetoUnion] | None = None
