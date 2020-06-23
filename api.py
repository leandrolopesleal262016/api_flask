from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

banco = sqlite3.connect('telefones.db')
cursor = banco.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS validos  (id INTEGER PRIMARY KEY AUTOINCREMENT,tel integer UNIQUE)")
cursor.execute("CREATE TABLE IF NOT EXISTS bloqueados (id INTEGER PRIMARY KEY AUTOINCREMENT,tel integer UNIQUE)")


def insere_valido(tel):  # Isere numeros na tabela validos

    try:

        banco = sqlite3.connect('telefones.db')
        cursor = banco.cursor()
        query = ("INSERT INTO validos VALUES (NULL,'{}')").format(tel)
        cursor.execute(query)
        banco.commit()
        cursor.close()
        banco.close()

    except Exception as err:

        print(err)


def insere_bloqueado(tel):  # Isere numeros na tabela bloqueados

    try:

        banco = sqlite3.connect('telefones.db')
        cursor = banco.cursor()
        query = ("INSERT INTO bloqueados VALUES (NULL,'{}')").format(tel)
        cursor.execute(query)
        banco.commit()
        cursor.close()
        banco.close()

    except Exception as err:

        print(err)
        return ("erro")


def remove_valido(tel):  # Remove numeros da tabela validos

    telefones_validos = validos_cadastrados()

    for item in telefones_validos:

        n = telefones_validos.index(item)
        elemento = telefones_validos[n]
        elemento = elemento[1]

        print("Elemento encontrado", elemento)

        if tel == elemento:

            try:

                banco = sqlite3.connect('telefones.db')
                cursor = banco.cursor()
                query = ("DELETE FROM validos WHERE tel = '{}'").format(tel)
                cursor.execute(query)
                banco.commit()
                cursor.close()
                banco.close()

                txt = ("Removido o numero {} da tabela validos").format(tel)
                return jsonify(txt), 200

            except Exception as err:

                print(err)
                return ("erro ao tentar remover")

    print("Este numero nao esta nalista de validos")
    return ("erro")


def remove_bloqueado(tel):  # Remove numeros da tabela bloqueados

    telefones_bloqueados = bloqueados_cadastrados()

    for item in telefones_bloqueados:

        n = telefones_bloqueados.index(item)
        elemento = telefones_bloqueados[n]
        elemento = elemento[1]

        print("Elemento encontrado", elemento)

        if tel == elemento:

            try:

                banco = sqlite3.connect('telefones.db')
                cursor = banco.cursor()
                query = ("DELETE FROM bloqueados WHERE tel = '{}'").format(tel)
                cursor.execute(query)
                banco.commit()
                cursor.close()
                banco.close()

                txt = ("Removido o numero {} da tabela bloqueio").format(tel)
                return jsonify(txt), 200

            except Exception as err:

                print(err)
                return ("erro ao tentar remover")

    print("Este numero nao esta nalista de bloqueio")
    return ("erro")


def validos_cadastrados():  # Retorna numeros de telefone da tabela validos

    try:

        banco = sqlite3.connect('telefones.db')
        cursor = banco.cursor()
        query = ("SELECT * FROM validos")
        cursor.execute(query)
        validos = cursor.fetchall()
        cursor.close()
        banco.close()

        return validos

    except Exception as err:

        print(err)
        return ("erro")


def bloqueados_cadastrados():  # Retorna numeros de telefone da tabela bloqueados

    try:

        banco = sqlite3.connect('telefones.db')
        cursor = banco.cursor()
        query = ("SELECT * FROM bloqueados")
        cursor.execute(query)
        bloqueados = cursor.fetchall()
        cursor.close()
        banco.close()

        return bloqueados  # Editar antes de retornar

    except Exception as err:

        print(err)
        return ("erro")


telefones_validos = validos_cadastrados()  # Atualiza os dados da tabela validos na variavel telefones_validos
telefones_bloqueados = bloqueados_cadastrados()  # Atualiza os dados da tabela validos na variavel telefones_validos


@app.route('/telefones/', methods=['POST'])  # Verifica se 1 ou n telefones sao validos para discagem
def save_tel():
    telefones = request.get_json('tel')
    print("telefones recebidos", telefones, type(telefones))
    lista_bloqueados = []
    lista_validos = []
    lista_not_found = []

    telefones_validos = validos_cadastrados()
    telefones_bloqueados = bloqueados_cadastrados()

    for num in telefones:

        not_found = 1

        for item in telefones_bloqueados:

            n = telefones_bloqueados.index(item)
            elemento = telefones_bloqueados[n]
            elemento = elemento[1]

            if num == elemento:
                _bloqueados = ("{} : bloqueado").format(num)
                lista_bloqueados.append(_bloqueados)
                not_found = 0

        for item in telefones_validos:

            n = telefones_validos.index(item)
            elemento = telefones_validos[n]
            elemento = elemento[1]

            if num == elemento:
                _valido = ("{} : valido").format(num)
                lista_validos.append(_valido)
                not_found = 0

        if not_found == 1:
            nf = ("{} : nao_encontrado").format(num)
            lista_not_found.append(nf)


    print(lista_bloqueados)
    print(lista_validos)
    print(lista_not_found)

    return jsonify(lista_bloqueados, lista_validos, lista_not_found), 200


@app.route('/telefones/', methods=['PUT'])  # Insere 1 ou n telefones na lista de bloqueio
def bloquear_tel():
    telefones = request.get_json('tel')
    print("telefones recebidos para cadastrar em bloqueio", telefones, type(telefones))
    lista_bloqueados = []
    lista_validos = []

    telefones_validos = validos_cadastrados() # Telefones vindos do banco
    telefones_bloqueados = bloqueados_cadastrados()

    for num in telefones: #"telefones" - vindos do post

        tam = int(len(telefones_validos))
        print("telefones_validos",telefones_validos)

        if tam > 0:

            for item in telefones_validos: # Vindos do banco

                n = telefones_validos.index(item)
                elemento = telefones_validos[n]
                elemento = elemento[1]

                #print("Recebido do post", num)
                #print("Encontrado em validos", elemento)

                if num == elemento: # Se o vindo do post for igual ao vindo do banco

                    print("removendo numero da tabela validos")
                    remove_valido(num)
                    print("Inserindo numero na tabela bloqueados")
                    insere_bloqueado(num)

                else:

                    insere_bloqueado(num)

        else:  # Caso ainda nao houver nenhum item na lista de validos

            print("Inserido primeiros registros da lista")

            insere_bloqueado(num)

    return jsonify("Telefones inseridos na lista de bloqueio"), 200


@app.route('/telefones/', methods=['DELETE'])  # Remove 1 ou n telefones da lista de bloqueio
def remove_telefones():
    telefones = request.get_json('tel')
    print("telefones recebidos para remover do bloqueio", telefones, type(telefones))
    lista_bloqueados = []
    lista_validos = []

    telefones_validos = validos_cadastrados()
    telefones_bloqueados = bloqueados_cadastrados()

    for num in telefones:

        for item in telefones_bloqueados:

            n = telefones_bloqueados.index(item)
            elemento = telefones_bloqueados[n]
            elemento = elemento[1]

            if num == elemento:

                remove_bloqueado(num)
                insere_valido(num)

            else:

                remove_bloqueado(num)

    return jsonify("Telefones removidos da lista de bloqueio"), 200


@app.route('/telefones/', methods=['GET'])  # Retorna todos os telefones cadastrados (validos e bloqueados)
def home():
    telefones_validos = validos_cadastrados()
    telefones_bloqueados = bloqueados_cadastrados()

    lista_bloqueados = []
    lista_validos = []

    try:

        for item in telefones_bloqueados:
            n = telefones_bloqueados.index(item)
            elemento = telefones_bloqueados[n]
            elemento = elemento[1]

            lista_bloqueados.append(elemento)

        lista_bloqueados = ({"Lista Bloqueados": lista_bloqueados})

        for item in telefones_validos:
            n = telefones_validos.index(item)
            elemento = telefones_validos[n]
            elemento = elemento[1]

            lista_validos.append(elemento)

    except Exception as err:

        print(err)
        return jsonify("Listas vazias")

    lista_validos = ({"Lista Validos": lista_validos})

    print(lista_validos)
    print(lista_bloqueados)

    return jsonify(lista_validos, lista_bloqueados), 200


if __name__ == '__main__':
    app.run(debug=True)