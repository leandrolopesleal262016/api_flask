# api_flask
Api Flask Agente Virtual de Telefonia

API Rest em Python utilizando Flask para a verificação se um ou mais telefones podem ou não ter acionamentos.

A API utiliza SQLite para armazenamento dos dados e cria um banco de nome "telefones.db" contendo 2 tabelas: "validos" e "bloqueados",
onde serão cadastrados, alterados ou removidos via requisição HTTP.

# A API tem as seguintes funções: 

  GET - Retorna 2 listas: "Lista validos" e "Lista bloqueados" somando todos os telefones cadastrados

  POST - Envia n telefones para serem consultados e retorna um dicionario contendo o numero do telefone como chave e seu estado como      valor, podendo ser seu estado: "valido", "bloqueado" ou "nao_encontrado" (para o caso do telefone pesquisado não estar em nenhuma das duas tabelas)

  PUT - Insere n telefones na lista bloqueados

  DELETE - Remove n telefones da lista bloqueados (os telefones removidos da tabela bloqueados vão automaticamente para a tabela validos)

Enviar os telefones como uma lista (Ex. [11111111,22222222,33333333]), fazer requisiçoes para a url:

  127.0.0.1:5000/telefones/

# Requisitos

  Phython 3
  flask-1.1.2
  sqlite3
  
# Rodando a aplicação

  Executar o script api.py
