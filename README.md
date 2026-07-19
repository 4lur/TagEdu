# S.G.I.E. - Sistema de Gestão Integrada Escolar

## Descrição
O **S.G.I.E. (Sistema de Gestão Integrada Escolar)** é uma API RESTful desenvolvida para facilitar e centralizar o gerenciamento de rotinas escolares. O sistema oferece recursos para controle de alunos, emissão de documentos (como carteirinhas em PDF), registro de advertências disciplinares e autenticação segura de usuários.

## Tecnologias
O projeto foi desenvolvido utilizando as seguintes tecnologias e bibliotecas principais:
- **Python 3**
- **FastAPI**: Framework web de alta performance para construção de APIs.
- **PostgreSQL**: Banco de dados relacional.
- **psycopg2-binary**: Driver de conexão do PostgreSQL para Python.
- **Pydantic**: Validação de dados e serialização.
- **python-jose & bcrypt**: Gerenciamento de tokens JWT e criptografia de senhas para autenticação segura.
- **ReportLab**: Geração de documentos PDF dinâmicos (carteirinhas de estudantes).
- **Uvicorn**: Servidor ASGI para rodar a aplicação.
- **python-dotenv**: Gerenciamento de variáveis de ambiente.

## Arquitetura
O sistema segue uma arquitetura modularizada, baseada nos princípios de separação de responsabilidades (adaptando conceitos de MVC e Clean Architecture para o ecossistema FastAPI), facilitando a manutenção e escalabilidade.

A estrutura de diretórios é organizada da seguinte forma:
- `app/`: Diretório principal da aplicação.
  - `main.py`: Ponto de entrada da aplicação, onde o FastAPI é inicializado e as rotas são registradas.
  - `database.py`: Configurações de conexão e comunicação com o banco de dados PostgreSQL.
  - `models.py`: Definição das entidades e schemas de dados utilizando Pydantic.
  - `routes/`: Controladores de rotas, separados por domínio de negócio (`alunos.py`, `advertencias.py`, `auth.py`).
  - `utils/`: Módulos utilitários compartilhados, como geração de PDF (`pdf_generator.py`) e regras de autenticação (`auth.py`).

## Funcionalidades Principais
- **Autenticação e Autorização**: Login de usuários e emissão de tokens JWT para proteção de rotas restritas.
- **Gestão de Alunos**: Listagem geral de alunos matriculados e consulta detalhada por identificador.
- **Emissão de Documentos**: Geração de carteirinhas de estudantes em formato PDF, prontas para download.
- **Gestão de Advertências**: Registro, controle e listagem de advertências disciplinares, associando o aluno ao motivo e ao professor responsável.

## Documentação da API

| Rota | Método HTTP | Descrição |
|---|---|---|
| `/auth/login` | `POST` | Realiza a autenticação do usuário e retorna um token de acesso (JWT). |
| `/alunos/` | `GET` | Lista todos os alunos cadastrados no sistema. (Requer autenticação com token) |
| `/alunos/{aluno_id}` | `GET` | Retorna os detalhes de um aluno específico através do seu ID. |
| `/alunos/{aluno_id}/carteirinha` | `GET` | Gera e faz o download da carteirinha do aluno em formato PDF. |
| `/advertencias/` | `GET` | Lista todo o histórico de advertências cadastradas. |
| `/advertencias/` | `POST` | Registra uma nova advertência para um aluno específico. |

*A documentação interativa completa (Swagger UI) pode ser acessada em `/docs` com a API em execução.*

## Modelagem de Dados
O sistema manipula as seguintes entidades principais:

- **Aluno**: Representa o estudante, contendo `id`, `nome_completo`, `matricula`, `data_nascimento`, `serie`, `turma` e `instituicao`.
- **Advertência**: Representa uma infração disciplinar, contendo `id`, `aluno_id` (chave estrangeira referenciando o Aluno), `data_emissao`, `motivo` e `professor_responsavel`.
- **Usuário**: Entidade para controle de acesso ao sistema, verificada na rota de login (`username` e `hashed_password`).

## Instalação e Setup

Siga os passos abaixo para executar o projeto em seu ambiente local:

### 1. Pré-requisitos
- Python 3.8+ instalado em sua máquina.
- Banco de dados PostgreSQL rodando localmente.

### 2. Clonar o repositório
```bash
git clone <url-do-repositorio>
cd S.G.I.E
```

### 3. Configuração do Ambiente Virtual
Crie e ative um ambiente virtual para isolar as dependências do projeto:
```bash
# Criar ambiente virtual
python3 -m venv .venv

# Ativar no Linux/macOS
source .venv/bin/activate

# Ativar no Windows
.venv\Scripts\activate
```

### 4. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 5. Configuração do Banco de Dados
Certifique-se de que o PostgreSQL está rodando e crie o banco de dados. O arquivo `app/database.py` possui as seguintes credenciais configuradas:
- **Host**: `127.0.0.1` (Porta: `5432`)
- **Usuário**: `gestor_escola`
- **Senha**: `engredes`
- **Database**: `escola_db`

> **Atenção:** Em um ambiente de produção, é altamente recomendável utilizar variáveis de ambiente (via arquivo `.env` e a biblioteca `python-dotenv`) para proteger as credenciais de acesso ao banco de dados.

Para criar a estrutura de tabelas e inserir dados iniciais, execute o script de povoamento:
```bash
python povoar_banco.py
```

### 6. Executar a Aplicação
Inicie o servidor de desenvolvimento com o Uvicorn:
```bash
uvicorn app.main:app --reload
```
A API estará acessível em: `http://127.0.0.1:8000`
