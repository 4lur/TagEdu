import os
import psycopg2
from psycopg2 import Error

def popular_banco():
    try:
        # Conecta ao banco de dados
        conn = psycopg2.connect(
            user=os.getenv("USER_DATABASE"),
            password=os.getenv("PASSWORD_DATABASE"),
            host=os.getenv("HOST_DATABASE"),
            port=os.getenv("PORT_DATABASE"),
            database=os.getenv("DATABASE")
        )
        cur = conn.cursor()

        # Dados Mock
        alunos_mock = [
            ('João Silva', '2024001', '2010-05-15', '1º Ano', 'A', 'CEM 10'),
            ('Maria Oliveira', '2024002', '2011-08-22', '2º Ano', 'B', 'CEM 10'),
            ('Carlos Santos', '2024003', '2010-02-10', '3º Ano', 'C', 'CEM 10')
        ]

        # Inserindo os dados SQL
        for aluno in alunos_mock:
            query_insercao = """
            INSERT INTO alunos (nome_completo, matricula, data_nascimento, serie, turma, instituicao) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """

        # Executando iserção para cada aluno
        for aluno in alunos_mock:
            cur.execute(query_insercao, aluno)
            print(f"Aluno {aluno[0]} inserido com sucesso!")
        # Confirmando alteração no banco
        conn.commit()
    
    except (Exception, Error) as error:
        print(f"Erro ao conectar ou inserir no PostgreSQL: {error}")
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Conexao com o banco fechada.")

if __name__ == "__main__":
    popular_banco()