from app.utils.pdf_generator import gerar_pdf_carteirinha
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.utils.auth import obter_usuario_atual
from psycopg2.extras import RealDictCursor
from app.database import get_db_connection
from app.models import Aluno
from typing import List

router = APIRouter()

# Rota para listar todos os alunos
@router.get("/", response_model=List[Aluno])
def listar_alunos(usuario: str = Depends(obter_usuario_atual)):
    if not usuario:
        raise HTTPException(status_code=401, detail="Token invalido")
    
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Erro ao conectar no banco")
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, nome_completo, matricula, data_nascimento, serie, turma, instituicao FROM alunos")
    alunos = cur.fetchall()

    cur.close()
    conn.close()

    return alunos

# Rota para buscar um aluno específico
@router.get("/{aluno_id}", response_model=Aluno)
def buscar_aluno(aluno_id: int):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Erro ao conectar no banco")
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, nome_completo, matricula, data_nascimento, serie, turma, instituicao FROM alunos WHERE id=%s", (aluno_id,))

    aluno = cur.fetchone()

    cur.close()
    conn.close()

    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno nao encontrado")
    
    return aluno

# Rota para buscar a carteirinha
@router.get("/{aluno_id}/carteirinha")
def gerar_carteirinha_aluno(aluno_id: int):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Erro ao conectar no banco")
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM alunos WHERE id=%s", (aluno_id,))
    
    aluno = cur.fetchone()

    cur.close()
    conn.close()

    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno nao encontrado")
    
    pdf_buffer = gerar_pdf_carteirinha(aluno)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=carteirinha_{aluno['matricula']}.pdf"})