from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# Pydantic Model para Aluno
class Aluno(BaseModel):
    id: int
    nome_completo: str
    matricula: str
    data_nascimento: date
    serie: str
    turma: str
    instituicao: str

# Pydantic Model para registro de advertências
class Advertencia(BaseModel):
    aluno_id: int
    motivo: str
    professor_responsavel: str

# Pydantic Model para resposta de advertência
class AdvertenciaResponse(BaseModel):
    id: int
    aluno_id: int
    data_emissao: datetime
    motivo: str
    professor_responsavel: str