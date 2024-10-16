# Projeto Computação em Nuvem - Insper 2024.2
**Feito por Luca Caruso**

**Projeto: Consulta de Cotações e Gerenciamento de Usuários com FastAPI**

## 📄 Explicação do Projeto
Este projeto implementa uma API usando FastAPI para gerenciar usuários (registro, login) e consultar cotações de empresas via API do Yahoo Finance.

## 📸 Screenshot dos Endpoints Testados

## 📹 Vídeo de Execução da Aplicação
[![Assistir ao vídeo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)](https://www.youtube.com/watch?v=xvFZjo5PgG0)

## 🚀 Como Executar a Aplicação

### Pré-requisitos:
- **Docker** instalado.
- **PostgreSQL** configurado.

### Passos para executar a aplicação:
1. Clone este repositório:
   ```bash
   https://github.com/LuCaruso/ProjetoCloud.git
   cd ProjetoCloud

2. Criar ambiente virtual
3. Baixar dependências
    ```bash 
    pip install -r requirements.txt

4. Configure o arquivo .env com suas credenciais:
   ```bash
    SECRET_KEY = "secret"
    DATABASE_URL= "postgresql://user:password@localhost/dbname"

## 📋 Documentação dos Endpoints da API
| Método  | Rota          | Descrição                          |
|---------|---------------|------------------------------------|
| `POST`  | `/registrar/`  | Registrar um novo usuário          |
| `POST`  | `/login/`      | Login e obtenção do token JWT      |
| `GET`   | `/consultar/`  | Consultar a cotação de uma empresa |

## 📊 Diagramas de Fluxo (Mermaid)

### Explicação do fluxo:

- **Registro**:
  - O usuário envia um `POST /registrar` com os dados de registro.
  - Exemplo de JSON para Registro de Usuário:
    ```json
    {
        "nome": "Disciplina Cloud",
        "email": "cloud@insper.edu.br",
        "senha": "cloud0"
    }
  - A API verifica se o e-mail já existe no banco de dados.
    - Se o e-mail já está registrado, retorna um código de status `409` (conflito).
    - Caso contrário, a API cria o novo usuário e retorna um token JWT para o usuário recém-registrado.

- **Login**:
  - O usuário envia um `POST /login` com suas credenciais.
  - Exemplo de JSON para Login:
    ```json
    {
        "email": "cloud@insper.edu.br",
        "senha": "cloud0"
    }
  - A API verifica as credenciais no banco de dados e, se forem válidas, retorna um token JWT.

- **Consulta**:
  - O usuário envia um `GET /consultar?empresa=XYZ` com o `ticker` da empresa desejada. Exemplos: AAPL, MSFT, PETR4.SA..
  - Exemplo de resposta para consulta de cotação:
    ```json
    {
      "usuario": "Disciplina Cloud",
      "empresa": "Apple Inc.",
      "Ticker": "AAPL",
      "cotacao_atual": 233.85000610351562,
      "pe_ratio": 31.26337,
      "dividend_yield": 0.0043,
      "market_cap": 3555478994944,
      "roe": 1.60583
    }
  - A API verifica se o usuário está autenticado usando o token JWT.
    - Se o usuário for encontrado, a API consulta os dados da empresa e retorna as informações de cotação.

```mermaid
sequenceDiagram
    participant Usuário
    participant API
    participant BancoDeDados
    Usuário->>API: POST /registrar
    API->>BancoDeDados: Verifica se email já existe
    alt Email já registrado
        API->>Usuário: 409 Email já registrado
    else
        API->>BancoDeDados: Cria novo usuário
        BancoDeDados->>API: Usuário criado
        API->>Usuário: JWT Token (usuário registrado)
    end
    
    Usuário->>API: POST /login
    API->>BancoDeDados: Verifica credenciais
    BancoDeDados->>API: Credenciais válidas
    API->>Usuário: JWT Token (login)
    
    Usuário->>API: GET /consultar?empresa=XYZ
    API->>BancoDeDados: Verifica usuário com token
    BancoDeDados->>API: Usuário encontrado
    API->>API: Consulta dados da empresa
    API->>Usuário: Retorna dados da empresa (cotação)
