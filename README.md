## Flask

`pipenv install flask`

O Flask permite que algumas variáveis sejam acessíveis de forma global pelas threads do servidor, onde cada uma dessas variáveis terá um valor correspondente ao contexto da thread.

Em conssonância a isso, há 2 contexto de variáveis globais no Flask: **contexto de aplicação** e **contexto de requisição**.

### Contexto de Aplicação

#### current_app

`from flask import current_app`

A variável **current_app** é uma variável do **contexto de aplicação**. Ela é uma instância da aplicação flask (variável **app**).

#### g

`from flask import g`

A variável **g** é uma variável do **contexto de aplicação**. Ela pode ser utilizada para armazenar valores de forma global, onde módulos da aplicação podem ter acesso.

### Contexto de Requisição

#### request

`from flask import request`

A variável **request** é uma variável do **contexto de requisição**. Ela armazena todas as informações da requisição de um cliente.

#### session

`from flask import request`

A variável **session** é uma variável do **contexto de requisição**. Ela pode ser utilizada para armazenar valores de forma global, para aquela seção de requisição.

## Flask Restful

`pipenv install flask-restful`

`from flask_restful import Resource, reqparse, fields, marshal_with`

`api.add_resource(Resource, "uri_1", "uri_2")`

## Flask Migrate

`pipenv install flask-migrate`

1. Criar a pasta **migrations** com o comando `flask db init`.
2. Fazer as alterações necessárias nas classes dos Models do banco de dados.
3. Gerar uma migração automática utilizando `flask db migrate`.
4. Revisar o script gerado e corrigi-lo caso seja necessário.
5. Aplicar as alterações no banco de dados com o comando `flask db upgrade`.

Na primeira migração, o comando `flask db migrate` faz a mesma coisa que o comando `db.create_all()` faria, ou seja, inicializa o banco de dados. No entanto, nas outras migrações, aquele comando somente irá atualizar o que for necessário, preservando o conteúdo do banco de dados.
