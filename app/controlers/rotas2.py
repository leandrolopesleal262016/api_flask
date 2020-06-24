from app import app,db
from flask import request,jsonify
from app.model.tabelas import TelModel

#cadastra 1 ou n telefones
#data:      {"telefones":["123","456","789","8569","965842"]}
#metodo:    PUT
@app.route('/api/telefones', methods=['PUT'])
def add():
    telefones = request.get_json()
    #validação de  strutura json
    if not "telefones" in telefones:
        return {"status":False,"message":"Key 'telefones' nao encontrada"}
    #validação de tipo de dados
    if False in [isinstance(x,str) for x in telefones["telefones"]]:
        return {"status":False,"message":"o tipo de dado valido e texto!"}

    #filtro de numeros não existentes
    existentes= [x.numero for x in TelModel.query.filter(TelModel.numero.in_(telefones["telefones"])).all()]
    novos = [x for x in telefones["telefones"] if x not in existentes]

    #inserção no banco de dados
    for num in novos:
        item = TelModel(num,0)
        db.session.add(item)
    db.session.commit()

    return f"{len(novos)} numeros novos carregados!"

#cadastra/remover 1 ou n telefones já existentes na lista de bloqueios
#data:      {"telefones":[{"numero":"123","status":true},{"numero":"456","status":false}]}
#metodo:    POST
@app.route('/api/telefones/update', methods=['POST'])
def update():
    {"telefones":[{"numero":"123","status":True}]}
    telefones = request.get_json()
    #validação de  strutura json
    if not "telefones" in telefones:
        return {"status":False,"message":"Key 'telefones' nao encontrada"}
    #validação de tipo de dados
    if False in [isinstance(x["numero"],str) for x in telefones["telefones"]]:
        return {"status":False,"message":"o tipo de dado valido para a key 'numero' e texto!"}
    #validação de tipo de dados
    if False in [isinstance(x["status"],bool) for x in telefones["telefones"]]:
        return {"status":False,"message":"o tipo de dado valido para a key 'status' e boleana!"}


    #filtro de numeros não existentes
    tels = [x["numero"] for x in telefones["telefones"]]
    db_lista = TelModel.query.filter(TelModel.numero.in_(tels)).all()
    existentes = [x.numero for x in db_lista]
    novos = [x for x in tels if x not in existentes]

    if novos:
        return {"status":False,"message":f"numeros nao encontrados:{','.join(novos)}"}

    for num in telefones["telefones"]:
        tel = num["numero"]
        db_item = [x for x in db_lista if x.numero == tel][0]
        db_item.status = num["status"]
    db.session.commit()

    return {"status":True}

#consultar todos os telefones
#metodo:    GET
@app.route('/api/telefones', methods=['GET'])
def getvalues():
    result = [{"telefone":x.numero,"status":x.status} for x in TelModel.query.all()]
    return jsonify(result)

#consultar 1 ou n telefones para ferificar se sao validos para discagem
#data:      {"telefones":["123","456","789","8569","965842"]}
#metodo:    POST
@app.route('/api/telefones/validos', methods=['POST'])
def check():
    telefones = request.get_json()
    #validação de  strutura json
    if not "telefones" in telefones:
        return {"status":False,"message":"Key 'telefones' nao encontrada"}
    #validação de tipo de dados
    if False in [isinstance(x,str) for x in telefones["telefones"]]:
        return {"status":False,"message":"o tipo de dado valido e texto!"}

    #filtro de numeros não existentes
    db_itens = TelModel.query.filter(TelModel.numero.in_(telefones["telefones"])).all()
    existentes= [x.numero for x in db_itens]
    novos = [x for x in telefones["telefones"] if x not in existentes]

    ["1","2","3","4","5"]
    [{"numero":"1","status":"NAO CADASTRADO"}]
    response = []

    for num in telefones["telefones"]:
        item = {"numero":num}
        item["status"] = "NAO CADASTRADO" if num in novos else [x for x in db_itens if x.numero == num][0].status
        response.append(item)
    
    return jsonify(response)



#alto volume de dados
# quando temos um grande volume de dados o importante é dividi-lo em partes (paginas)
# assim evitamos um alto processamento em um unico ponto e temos um melhor desenpenho 
# do sistema
