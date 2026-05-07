from flask import Flask, request, jsonify

app = Flask(__name__)

tarefas = []
contador = 1

def busca(tarefas, id):
    return next((t for t in tarefas if t['id'] == id), None)

@app.route("/tarefas", methods=['POST'])
def criar_tarefa():
    global contador
    dados = request.get_json()

    nova_tarefa = {
        "id": contador,
        "titulo": dados.get('titulo'),
        "descricao": dados.get('descricao', ''),
        "concluida": False
    }
    tarefas.append(nova_tarefa)
    contador += 1

    return jsonify(nova_tarefa), 201

@app.route("/tarefas", methods=['GET'])
def listar_tarefas():
    return jsonify(tarefas)

@app.route('/tarefas/<int:id>', methods=['GET'])
def buscar_tarefa(id):
    tarefa = busca(tarefas, id)
    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    return jsonify(tarefa)

@app.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    tarefa = busca(tarefas, id)
    if tarefa is None:
        return jsonify({"erro":"Tarefa não encontrada"}), 404

    dados = request.get_json()
    tarefa['titulo'] = dados.get('titulo', tarefa['titulo'])
    tarefa['descricao'] = dados.get('descricao', tarefa['descricao'])
    tarefa['concluida'] = dados.get('concluida', tarefa['concluida'])

    return jsonify(tarefa)

@app.route('/tarefas/<int:id>', methods=['DELETE'])
def deletar_tarefa(id):
    global tarefas
    tarefa = busca(tarefas, id)
    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    tarefas = [t for t in tarefas if t['id'] != id]
    return jsonify({"mensagem": "Tarefa removida"}), 200
    