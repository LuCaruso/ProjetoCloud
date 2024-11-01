# Projeto Computação em Nuvem - Insper 2024.2
**Feito por Luca Caruso**

**Projeto: Consulta de Cotações e Gerenciamento de Usuários com FastAPI**

## 📄 Explicação do Projeto
Este projeto implementa uma API usando FastAPI para gerenciar usuários (registro, login) e consultar cotações de empresas via API do Yahoo Finance.

## 📸 Screenshot dos Endpoints Testados
Registrando um usuário
![Screenshot do Registro](image.png)

Realizando Login
![Screenshot do Login](image-1.png)

Autorizando a consulta com o token
![Screenshot da autorização concedida](image-2.png)

Consultando a cotação
![Screenshot da consulta a cotação da AAPL](image-3.png)


## 📹 Vídeo de Execução da Aplicação
[![Assistir ao vídeo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)](https://youtu.be/l1l29sYtqLw)

## 🚀 Como Executar a Aplicação

### Pré-requisitos:
- **Docker** instalado.
- **PostgreSQL** configurado.

### Passos para executar a aplicação:

1. Baixe o compose na sua máquina


    Para configurar a aplicação, você pode baixar o arquivo `compose.yaml` [clicando aqui](./compose.yaml).

    Ou, utilize o botão abaixo para fazer o download direto:

    [![Baixar YAML](https://img.shields.io/badge/Baixar-YAML-blue?style=for-the-badge&logo=download&logoColor=white)](./compose.yaml)


2. Configure o arquivo .env com suas credenciais:[OPCIONAL]
   ```bash
    DATABASE_PASSWORD=<sua senha>
    DATABASE_USER=<seu usuario>
    DATABASE_NAME=<seu database>
    SECRET_KEY=<segredo de criptografia>
    ```

## 📋 Documentação dos Endpoints da API
| Método  | Rota          | Descrição                          |
|---------|---------------|------------------------------------|
| `POST`  | `/registrar/`  | Registrar um novo usuário          |
| `POST`  | `/login/`      | Login e obtenção do token JWT      |
| `GET`   | `/consultar/`  | Consultar a cotação de uma empresa |

## 📊 Diagramas de Fluxo (Mermaid)
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
```
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
    ```
  - A API verifica se o e-mail já existe no banco de dados.
    - Se o e-mail já está registrado, retorna um código de status `409` (conflito).
    - Caso contrário, a API cria o novo usuário e retorna um token JWT para o usuário recém-registrado.
    
  Para testar rode no terminal:
  ```bash
  curl -X POST "http://127.0.0.1:8000/registrar/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"nome\": \"Disciplina Cloud\", \"email\": \"cloud@insper.edu.br\", \"senha\": \"cloud0\"}"
  ```

- **Login**:
  - O usuário envia um `POST /login` com suas credenciais.
  - Exemplo de JSON para Login:
    ```json
    {
        "email": "cloud@insper.edu.br",
        "senha": "cloud0"
    }
  - A API verifica as credenciais no banco de dados e, se forem válidas, retorna um token JWT.
  
  Para testar rode no terminal:
  ```bash
  curl -X POST "http://127.0.0.1:8000/login/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"email\": \"cloud@insper.edu.br\", \"senha\": \"cloud0\"}"
  ```


- **Consulta**:
  - O usuário envia um `GET /consultar?empresa=XYZ` com o `ticker` da empresa desejada. Exemplos: AAPL, MSFT, PETR4.SA..
  - Caso o usuário não selecionar nenhuma empresa, por padrão a API retornará a cotação da Apple Inc.
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
  
  Para testar rode no terminal:
  ```bash
  curl -X GET "http://127.0.0.1:8000/consultar/?empresa=AAPL" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsIm5hbWUiOiJEaXNjaXBsaW5hIENsb3VkIiwiaWF0IjoxNzMwNDI3MDY4fQ.y61gvTO8yH9WDmePsF3Psxz0YVAiyX1qI51ZeG-fvNY"
  ```



