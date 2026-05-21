from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da Tabela
class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=True)
    concluida = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'concluida': self.concluida
        }

# Criar as tabelas (roda uma vez só)
with app.app_context():
    db.create_all()

@app.route("/")
def inicio():
    return("<p>Isso aqui é uma API</p>")

@app.route("/tarefas", methods=['POST'])
def criar_tarefa():
    dados = request.get_json()

    if not dados.get('titulo'):
        return jsonify({"erro": "Título é obrigatório"}), 400

    nova_tarefa = Tarefa(
        titulo=dados['titulo'],
        descricao=dados.get('descricao', ''),
        concluida=dados.get('concluida', False)
    )

    db.session.add(nova_tarefa)
    db.session.commit()

    return jsonify(nova_tarefa.to_dict()), 201

@app.route("/tarefas", methods=['GET'])
def listar_tarefas():
    todas = Tarefa.query.all()
    return jsonify([t.to_dict() for t in todas])

@app.route('/tarefas/<int:id>', methods=['GET'])
def buscar_tarefa(id):
    tarefa = Tarefa.query.get(id)
    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    return jsonify(tarefa.to_dict())

@app.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    tarefa = Tarefa.query.get(id)
    if tarefa is None:
        return jsonify({"erro":"Tarefa não encontrada"}), 404

    dados = request.get_json()

    if 'titulo' in dados:
        tarefa.titulo = dados['titulo']
    if 'descricao' in dados:
        tarefa.descricao = dados['descricao']
    if 'concluida' in dados:
        tarefa.concluida = dados['concluida']

    db.session.commit()

    return jsonify(tarefa.to_dict())

@app.route('/tarefas/<int:id>', methods=['DELETE'])
def deletar_tarefa(id):
    tarefa = Tarefa.query.get(id)
    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    db.session.delete(tarefa)
    db.session.commit()
    return jsonify({"mensagem": "Tarefa removida"}), 200
    