from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/clientes'

cors = CORS(app)
db = SQLAlchemy(app)

class Dado(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(20))
    telefone = db.Column(db.String(12))
    cep = db.Column(db.String(10))
    rua = db.Column(db.String(30))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(20))
    bairro = db.Column(db.String(20))
    cidade = db.Column(db.String(10))
    uf = db.Column(db.String(10))

    def to_json(self):
        return {"id": self.id, "email": self.email, "senha": self.senha, "telefone": self.telefone, "cep": self.cep, "rua": self.rua, "numero": self.numero, "complemento": self.complemento, "bairro": self.bairro, "cidade": self.cidade, "uf": self.uf}

@app.route("/clientes", methods=["GET"])
def seleciona_clientes():
    clientes_objetos = Dado.query.all()
    clientes_json = [clientes.to_json() for clientes in clientes_objetos]
    print(clientes_json)
    return gera_response(200, "clientes", clientes_json, "Foi")


@app.route("/clientes/<id>", methods=["GET"])
def seleciona_cliente(id):
    clientes_objetos =  Dado.query.filter_by(id=id).first()
    clientes_json = clientes_objetos.to_json()
    
    return gera_response(200, "clientes", clientes_json, "Achado o Id")

@app.route("/clientes", methods=["POST"])
def cria_cliente():
    body = request.get_json()


    try:
        clientes = Dado(nome=body["nome"], email=body["email"], senha=body["senha"], telefone=body["telefone"], 
        cep=body["cep"], rua=body["rua"], numero=body["numero"], complemento=body["complemento"], bairro=body["bairro"], cidade=body["cidade"], uf=body["uf"])
        db.session.add(clientes)
        db.session.commit()
        return gera_response(201, "clientes", clientes.to_json(), "criado com sucesso")
    except Exception as e:
        print('erro', e)
        return gera_response(400, "clientes", {}, "Erro ao cadastrarr")


@app.route("/clientes/<id>", methods=["PUT"])
def atualiza_usuario(id):
    clientes_objetos = Dado.query.filter_by(id=id).first()
    body = request.get_json()
    
    try:
        if('nome' in body):
            clientes_objetos.nome = body['nome']
        if('email' in body):
            clientes_objetos.email = body['email']
        if('senha' in body):
            clientes_objetos.senha = body['senha']
        if('telefone' in body):
            clientes_objetos.telefone = body['telefone']
        if('cep' in body):
            clientes_objetos.cep = body['cep']
        if('rua' in body):
            clientes_objetos.rua = body['rua']
        if('numero' in body):
            clientes_objetos.numero = body['numero']
        if('complemento' in body):
            clientes_objetos.complemento = body['complemento']
        if('bairro' in body):
            clientes_objetos.bairro = body['bairro']
        if('cidade' in body):
            clientes_objetos.cidade = body['cidade']
        if('uf' in body):
            clientes_objetos.uf = body['uf']
        
        db.session.add(clientes_objetos)
        db.session.commit()
        return gera_response(200, "clientes", clientes_objetos.to_json(), "Atualizado com sucesso")
    except Exception as e:
            print('Erro', e)
            return gera_response(400, "clientes", {}, "Erro ao atualizar")
    
#deletar
@app.route("/clientes/<id>", methods=["DELETE"])
def deleta_clientes(id):
    clientes_objetos = Dado.query.filter_by(id=id).first()

    try:
        db.session.delete(clientes_objetos)
        db.session.commit()
        return gera_response(200, "clientes", clientes_objetos.to_json(), "Usuario deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "clientes", {}, "Erro ao deletar o usuario")




def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body), status, mimetype="application/json")

app.run()