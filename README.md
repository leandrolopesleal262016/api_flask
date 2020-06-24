# API_FLASK
Api Flask Agente Virtual de Telefonia

API Rest em Python utilizando Flask para a verificação se um ou mais telefones podem ou não ter acionamentos.

A API utiliza SQLite para armazenamento dos dados e cria um banco de nome "telefones.db" contendo uma tabela onde temos a coluna 'numeros'
do tipo string e e a coluna 'status' do tipo boleana que indicara se o telefone é valido ou não para acionamento.

# A API tem as seguintes funções:

Consultar 1 ou n telefones para ferificar se sao validos para discagem

metodo:    POST
data:      {"telefones":["123","456","789","8569","965842"]}
url:       127.0.0.1:5000/api/telefones/validos


Cadastra 1 ou n telefones

metodo:    PUT
data:      {"telefones":["123","456","789","8569","965842"]}
url:       127.0.0.1:5000/api/telefones


Cadastra/remove 1 ou n telefones já existentes na lista de bloqueios 

metodo:    POST
data:      {"telefones":[{"numero":"123","status":true},{"numero":"456","status":false}]} 
url:       127.0.0.1:5000/api/telefones/update


Consultar todos os telefones

metodo:    GET
url:       127.0.0.1:5000/telefones/


# Para um alto volume de dados:

Quando temos um grande volume de dados o importante é dividi-lo em partes (paginas)
assim evitamos um alto processamento em um unico ponto e temos um melhor desenpenho 
do sistema

 
# Requisitos

Phython 3,
flask 1.1.2,
Flask-SQLAlchemy 2.4.3,
sqlite3
  
# Rodando a aplicação

Executar o script run.py 
