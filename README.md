# Magpy

As equipes de desenvolvimento sempre preferem usar as tecnologias mais recentes e modernas, para garantir que todos seus projetos estão usando as últimas versões disponíves dos pacotes, criamos uma ferramenta batizada de MagPy. A ferramenta recebe um nome de projeto, uma lista de pacotes e caso não for declarada, devolve a última versão de cada pacote.

# Inicializando localmente

## Criar o banco de dados

`./manage.py migrate`

## Inicializar

`./manage.py runserver`

Por padrão, irá funcionar em `http://127.0.0.1:8000/`

## Testar a aplicação

Você pode executar esses testes com o [k6](https://k6.io/). Para instalar o k6 basta [baixar o binário](https://github.com/loadimpact/k6/releases) para o seu sistema operacional (Windows, Linux ou Mac).

Para rodar os testes abertos, especifique a variável de ambiente "API_BASE" com o endereço base da API testada.

`k6 run -e API_BASE='http://localhost:8080/' tests-open.js`

# Rotas

### `GET /api/projects/`

Retorna todos os projetos cadastrados no banco.

RESPONSE STATUS -> HTTP 200 (ok)

Response:

    [
      {
        "name": "magpy",
        "packages": [
          {
            "name": "Django",
            "version": "3.2.6"
          }
        ]
      },
    ]

### `GET /api/projects/<str:project_name>/`

Retorna as informações do projeto de mesmo nome, não é case sensitive.
Caso o projeto não exista, será retornado o status 404.

RESPONSE STATUS -> HTTP 200 (ok)

    {
        "name": "titan",
        "packages": [
            {"name": "Django", "version": "3.2.5"},
            {"name": "graphene", "version": "2.0"}
        ]
    }

### `POST /api/projects/`

Rota destinada a criação de um projeto e seus pacotes.
Caso algum pacote não exista, ou a versão declarada deste seja incorreta, será retornado o Status 400.
Não é necessário especificar a versão do pacote, se a mesma for ignorada, assume-se que o cliente deseja utilizar a última versão.

RESPONSE STATUS -> HTTP 201 (created)

Body:

    {
        "name": "titan",
        "packages": [
            {"name": "Django"},
            {"name": "graphene", "version": "2.0"}
        ]
    }

Response:

    {
        "name": "titan",
        "packages": [
            {"name": "Django", "version": "3.2.5"},  // Usou a versão mais recente
            {"name": "graphene", "version": "2.0"}   // Manteve a versão especificada
        ]
    }

### `DELETE /api/projects/<str:project_name>/`

Deleta o projeto especificado por nome, não é case sensitive
Não há conteúdo no retorno da requisição.
Caso o projeto não exista, retornará Status 404.

RESPONSE STATUS -> HTTP 204 (no content)

## Tecnologias utilizadas 📱

- Django
- Django Rest Framework
- SQLite
- Heroku
- Requests
