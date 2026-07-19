import os
import psycopg2

# Conexão com o banco
def get_db_connection():
    try:
        conn = psycopg2.connect(
            user=os.getenv("USER_DATABASE"),
            password=os.getenv("PASSWORD_DATABASE"),
            host=os.getenv("HOST_DATABASE"),
            port=os.getenv("PORT_DATABASE"),
            database=os.getenv("DATABASE")
        )
        return conn
    except Exception as e:
        print(f"Erro de conexao: {e}")
        return None