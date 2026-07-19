from fastapi import FastAPI
from app.routes import alunos, advertencias, auth

# Inicialização da API
app = FastAPI(title="S.G.I.E - Sistema de Gerenciamento Integrado Escolar", 
              description="Sistema integrado de gerenciamento escolar",
              version="0.1.1"
              )

# Rotas da aplicação
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(alunos.router, prefix="/alunos", tags=["Alunos"])
app.include_router(advertencias.router, prefix="/advertencias", tags=["Advertencias"])

# Rota de boas-vindas
@app.get("/", tags=["Geral"])
def read_root():
    return{"mensagem": "API do Sistema Escolar Online!"}