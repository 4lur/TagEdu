from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db_connection
from app.utils.auth import verificar_senha, criar_token_jwt

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Erro ao conectar ao banco de dados"
        )
    cur = conn.cursor()
    cur.execute("SELECT username, hashed_password FROM usuarios WHERE username = %s",(form_data.username,))
    user = cur.fetchone()
    if not user or not verificar_senha(form_data.password, user[1]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Credenciais invalidas"
        )

    access_token = criar_token_jwt(data={"sub": user[0]})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
