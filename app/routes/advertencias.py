from fastapi import APIRouter, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from app.database import get_db_connection
from app.models import Advertencia, AdvertenciaResponse
from typing import List

router = APIRouter()

# Rota para listar todas as advertências
@router.get("/", response_model=List[AdvertenciaResponse])
def listar_advertencias():
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Erro ao conectar no banco")
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM advertencias")
    advertencias = cur.fetchall()

    cur.close()
    conn.close()

    return advertencias

# Rota para aplicar advertência
@router.post("/", status_code=201)
def aplicar_advertencia(nova_advertencia: Advertencia):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Erro ao conectar no banco")
    
    cur = conn.cursor()
    try:
        query = """
            INSERT INTO advertencias (aluno_id, motivo, professor_responsavel)
            VALUES(%s, %s, %s) RETURNING id, data_emissao;
        """
        
        valores = (nova_advertencia.aluno_id, nova_advertencia.motivo, nova_advertencia.professor_responsavel)
        
        cur.execute(query, valores)
        resultado = cur.fetchone()
        conn.commit()

        if resultado is None:
            raise HTTPException(status_code=500, detail="Erro interno: Nao foi possivel recuperar os dados da insercao.")

        return {
            "mensagem": "Advertencia registrada com sucesso!",
            "id_advertencia": resultado[0],
            "data_emissao": resultado[1]
        }
    
    except psycopg2.errors.ForeignKeyViolation:
        conn.rollback()
        raise HTTPException(status_code=404, detail="Aluno nao encontrado para aplicar a advertencia")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar: {str(e)}")
    finally:
        cur.close()
        conn.close()