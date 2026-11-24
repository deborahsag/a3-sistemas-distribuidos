from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database.database import inicializar_banco
from .routers import ideias, projetos

from .config import settings

# Inicializar banco de dados
inicializar_banco()

# Criar instância do FastAPI
app = FastAPI()

# Rotas de Ideias
app.include_router(ideias.router)
app.include_router(projetos.router)


# Conexão com o front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
