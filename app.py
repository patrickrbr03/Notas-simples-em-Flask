from flask import Flask

app = Flask(__name__)

tarefas = []
contador = 1

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

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

# @app.route("/tarefas", methods=['GET'])
# def listar_tarefas():
#     return jsonify(tarefas)


