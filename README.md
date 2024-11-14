# Projeto Computação em Nuvem - Insper 2024.2
**Feito por Luca Caruso**

**Link para o DockerHub do projeto:**
[Repositório Docker Hub](https://hub.docker.com/repository/docker/lc2020/projeto_cloud_lucac/general)

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

   Você também pode baixar a imagem do Docker Hub através deste comando:
   ```bash
   docker pull lc2020/projeto_cloud_lucac:v5
   ```

3. Configure o arquivo .env com suas credenciais:[OPCIONAL]
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


# 🌐 AWS

## 🔗 Acesso à API

Após concluir a configuração do cluster e o deploy da aplicação, você pode acessar a API através do seguinte link:

a89e5f05521544dafbae1856f247081d-838556397.us-east-1.elb.amazonaws.com

Para testar a API de forma interativa, utilize o Swagger:

a89e5f05521544dafbae1856f247081d-838556397.us-east-1.elb.amazonaws.com/docs

## 🚀 Tutorial para Subir um Cluster no AWS

Este guia explica detalhadamente como subir um cluster no AWS, passo a passo. Ele inclui a instalação de ferramentas necessárias, configuração do ambiente e comandos para a criação e deploy dos recursos.

## 1. Instalação do AWS CLI 🛠️

O AWS CLI é uma ferramenta que permite interagir com os serviços da AWS diretamente pelo terminal. Baixe e instale o AWS CLI através da [documentação oficial](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

Verifique a instalação executando no terminal:
```bash
aws --version
```
O resultado esperado deve ser semelhante a:
```bash
aws-cli/2.17.20 Python/3.11.6 Windows/10 exe/AMD64 prompt/off
```

## 2. Criação de Chave de Acesso 🔑

As chaves de acesso são necessárias para que o CLI possa autenticar e executar comandos na sua conta AWS. Para gerar uma chave:
- Acesse o console IAM: [IAM Console](https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-1#/users)
- Entre no seu usuário e vá para `Credenciais de Segurança > Chaves de Acesso`.
- Clique em `Criar chave de acesso`.
- Escolha `Interface de linha de comandos (CLI)` e prossiga.
- Faça o download do arquivo `.csv` com suas credenciais.

## 3. Configuração do AWS CLI ⚙️

O comando `aws configure` permite configurar suas credenciais para que a AWS CLI possa autenticar suas requisições.
No terminal, digite o comando:
```bash
aws configure
```
Preencha as credenciais conforme o arquivo `.csv` gerado anteriormente.

Para mais informações, consulte a [documentação oficial](https://docs.aws.amazon.com/pt_br/eks/latest/userguide/install-awscli.html).

## 4. Instalação do EKSCTL 🛡️

O `eksctl` é uma ferramenta de linha de comando específica para criar e gerenciar clusters do Amazon EKS.
Instale o `eksctl` para configurar o EKS via CLI:
```bash
choco install eksctl
```

**Observação**: Este comando deve ser executado com `permissões de administrador`.


Mais detalhes estão disponíveis na [documentação oficial do EKSCTL](https://eksctl.io/installation/).

## 5. Criação do Cluster 🏗️

Nesta etapa, você criará um cluster EKS com dois nós:
```bash
eksctl create cluster --name app-consultaCotacao --region us-east-1 --nodes 2 --node-type t3.medium
```

Depois, atualize a configuração do `kubeconfig` para que o `kubectl` possa se conectar ao cluster:
```bash
aws eks --region us-east-1 update-kubeconfig --name app-consultaCotacao
```

## 6. Criação do Arquivo `db-deployment.yaml` 📄

O arquivo `db-deployment.yaml` é um manifesto Kubernetes que define os recursos necessários para o deploy do banco de dados. Certifique-se de substituir as variáveis de ambiente conforme necessário.

Aqui está um exemplo do `db-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:17
        env:
          - name: POSTGRES_USER
            value: "projeto"
          - name: POSTGRES_PASSWORD
            value: "projeto"
          - name: POSTGRES_DB
            value: "projeto"
        ports:
          - containerPort: 5432
---
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  ports:
    - port: 5432
  selector:
    app: postgres
```

## 7. Criação do Arquivo `web-deployment.yaml` 🌐

Da mesma forma, o `web-deployment.yaml` é um arquivo que contém as definições para o deploy do aplicativo web. Atualize a imagem e as variáveis de ambiente de acordo com as suas necessidades.

Aqui está um exemplo do `web-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
      - name: fastapi
        image: lc2020/projeto_cloud_lucac:v5
        env:
          - name: SECRET_KEY 
            value: a5e6fda737aa4c22a9e80fb273aec1455a2bfc4854905ee0a2d5747b8272d6d5
          - name: DATABASE_HOST
            value: postgres
          - name: DATABASE_NAME
            value: projeto
          - name: DATABASE_USER
            value: projeto
          - name: DATABASE_PASSWORD
            value: projeto
        ports:
          - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 8000
  selector:
    app: fastapi
```


## 8. Aplicação dos Arquivos de Deploy 📦

Para aplicar as configurações e fazer o deploy dos recursos, navegue até a pasta onde os arquivos `.yaml` foram criados e execute:
```bash
kubectl apply -f db-deployment.yaml 
kubectl apply -f web-deployment.yaml
```
Este comando criará os recursos no cluster com base nas definições dos arquivos `.yaml`.

## 9. Verificando os Pods em Execução 🔍
Para verificar os pods em execução no cluster, execute:
```bash
kubectl get pods
```
Este comando listará todos os pods em execução, juntamente com seus status.
Se tuodo estiver certo os `status` aparacerão como `Running`

```bash
NAME                        READY   STATUS    RESTARTS   AGE
fastapi-f6867768c-w8hlg     1/1     Running   0          21s
postgres-795b65b965-776pl   1/1     Running   0          29s
```

## 10. Visualizando Logs para Depuração 🛠️
Para visualizar os logs de um pod específico, primeiro obtenha o nome do pod usando o comando kubectl get pods. Em seguida, execute:
```bash
kubectl logs <nome-do-pod>
```
Substitua `<nome-do-pod>` pelo nome do pod que você deseja inspecionar. Este comando exibirá os logs do pod, que podem ser úteis para depuração.

**Observação:** O nome do pod foi obtido na sessão anterior

## 11. Obtenção do Link de Acesso 🔗

Para acessar a aplicação via Load Balancer e obter o URL de serviço, execute:
```bash
kubectl get svc fastapi-service
```
Este comando retornará detalhes do serviço, incluindo o endereço de IP externo ou URL.
Use o URL fornecido para fazer as requisições via `Postman` ou `CURL`, ou acesse o link no navegador incluindo `/docs` no final para poder testar a aplicação no `Swagger`.

## 🛠️ Comandos CURL para Testar a Aplicação

### Registrar
```bash
curl -X POST "a89e5f05521544dafbae1856f247081d-838556397.us-east-1.elb.amazonaws.com/registrar/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"nome\": \"Disciplina Cloud\", \"email\": \"cloud@insper.edu.br\", \"senha\": \"cloud0\"}"
```

### Login
```bash
curl -X POST "a89e5f05521544dafbae1856f247081d-838556397.us-east-1.elb.amazonaws.com/login/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"email\": \"cloud@insper.edu.br\", \"senha\": \"cloud0\"}"
```

### Consulta
```bash
curl -X GET "a89e5f05521544dafbae1856f247081d-838556397.us-east-1.elb.amazonaws.com/consultar/?empresa=AAPL" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjYsIm5hbWUiOiJEaXNjaXBsaW5hIENsb3VkIiwiaWF0IjoxNzMwNjk4MzcyfQ.KrHyAc3GRbToDcE28qamN4IaGYoRsAtZFrSL0IfruAA"
```



