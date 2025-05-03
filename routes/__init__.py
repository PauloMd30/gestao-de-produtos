from flask import Blueprint, render_template

route_home = Blueprint("home", __name__)

@route_home.route("/")
def home():
     return render_template("index.html")

import os
from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, timedelta, date
from Database import Produto  
from bson.objectid import ObjectId, InvalidId  
from mongoengine import DoesNotExist, ValidationError
from dotenv import load_dotenv

load_dotenv()

numero_destino =os.environ.get('twilio_number2')




route_produto = Blueprint("produto", __name__)

@route_produto.route("/teste_envio")
def teste_envio():
    from whatsapp import enviar_mensagem_whatsapp
    numero = os.environ.get("twilio_number2")
    try:
        enviar_mensagem_whatsapp("Mensagem de teste do sistema!", numero)
        return "Mensagem enviada com sucesso!"
    except Exception as e:
        return f"Erro ao enviar: {e}"


# rota para consultar produtos com validade proxima
@route_produto.route("/consultar_por_validade_proxima")
def consultar_por_validade_proxima():
    hoje = date.today()
    data_limite = hoje + timedelta(days=7)
    query = Produto.objects(data_de_validade__lte=data_limite)
    produtos = [
        {
            'id': str(produto.id),
            'nome': produto.nome,
            'marca': produto.marca,
            'codigo_de_barras': produto.codigo_de_barras,
            'data_de_validade': produto.data_de_validade.strftime('%d/%m/%Y')  # Formatar a data
        }
        for produto in query
    ]
    return render_template("lista_produtos.html", PRODUTOS=produtos)



# inserindo um produto 
@route_produto.route("/", methods=["POST"])
def inserir_produto():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Dados inválidos ou ausentes."}), 400

    # Verifica e trata a data de validade
    try:
        try:
            data_de_validade = datetime.strptime(data["data validade"], '%d/%m/%Y').date()
        except ValueError:
            data_de_validade = datetime.strptime(data["data validade"], '%Y-%m-%d').date()
    except (KeyError, ValueError):
        return jsonify({"error": "Data de validade inválida ou ausente."}), 400

    # Validação da data de validade
    if data_de_validade < date.today():
        return jsonify({"error": "A data de validade não pode ser anterior à data atual."}), 400

    # Validação do código de barras
    codigo_de_barras = data.get("codigo de barras", "")
    if len(codigo_de_barras) != 13 or not codigo_de_barras.isdigit():
        return jsonify({"error": "O código de barras deve ter exatamente 13 dígitos numéricos."}), 400

    # Criação do produto
    try:
        novo_produto = Produto(
            nome=data["nome"],
            marca=data["marca"],
            codigo_de_barras=codigo_de_barras,
            data_de_validade=data_de_validade
        )
        novo_produto.save()
    except Exception as e:
        return jsonify({"error": f"Erro ao salvar o produto: {str(e)}"}), 500
    return jsonify({
            "message": "Produto inserido com sucesso.",
            "produto": {
            "nome": novo_produto.nome,
            "marca": novo_produto.marca,
            "codigo_de_barras": novo_produto.codigo_de_barras,
            "data_de_validade": novo_produto.data_de_validade.strftime('%Y-%m-%d')
            }
        }), 201

#obtendo todos produtos

@route_produto.route("/lista_produtos")
def listar_produtos():
    produtos = Produto.objects()
    for produto in produtos:
        produto.data_de_validade = produto.data_de_validade.strftime('%d/%m/%Y')
    return render_template("lista_produtos.html", PRODUTOS=produtos)


# envia um formulario para obter um novo produto
@route_produto.route("/novo")
def form_produto():
    return render_template("form_produto.html")

# edita um produto
@route_produto.route('/<string:produto_id>/edit')
def form_edit_produto(produto_id):
    try:
            produto = Produto.objects.get(id=ObjectId(produto_id))

    except (DoesNotExist, ValidationError, InvalidId):
            return jsonify({"mensagem":"Produto não encontrado ou ID inválido."}) , 404

    # Verifica se data_de_validade é datetime
    if isinstance(produto.data_de_validade, datetime):
        produto.data_de_validade = produto.data_de_validade.strftime('%Y-%m-%d')


    return render_template('form_produto.html', produto=produto)


@route_produto.route('/<string:produto_id>/update', methods=['POST'])
def atualizar_produto(produto_id):
    data = request.get_json()

    if data.get('_method') != 'PUT':
        return jsonify({"error": "Método não permitido."}), 405

    # Tenta converter e buscar o produto
    try:
        produto_editado = Produto.objects.get(id=ObjectId(produto_id))
    except (InvalidId, DoesNotExist, ValidationError):
        return jsonify({"error": "Produto não encontrado ou ID inválido."}), 404

    # Validação do código de barras (13 dígitos)
    codigo_barras = data.get('codigo de barras')
    if len(str(codigo_barras)) != 13 or not str(codigo_barras).isdigit():
        return jsonify({"error": "Código de barras deve ter exatamente 13 dígitos numéricos."}), 400

    # Validação da data de validade
    data_validade = data.get('data validade')
    try:
        data_validade = datetime.strptime(data_validade, '%Y-%m-%d').date()
        if data_validade < datetime.today().date():
            return jsonify({"error": "Data de validade não pode ser anterior à data atual."}), 400
    except (TypeError, ValueError):
        return jsonify({"error": "Data de validade no formato inválido."}), 400

    # Atualização
    produto_editado.nome = data['nome']
    produto_editado.marca = data['marca']
    produto_editado.codigo_de_barras = codigo_barras
    produto_editado.data_de_validade = data_validade

    produto_editado.save()

    return jsonify({
        "message": "Produto atualizado com sucesso.",
        "produto_id": str(produto_editado.id)
    })


# apaga um produto
@route_produto.route("/<string:produto_id>/delete", methods=["DELETE"])
def deletar_produto(produto_id):
    try:
        produto = Produto.objects.get(id=ObjectId(produto_id))
    except (DoesNotExist, ValidationError, InvalidId):
        return jsonify({"error": "Produto não encontrado ou ID inválido."}), 404
    produto.delete()
    return jsonify({'mensagem': 'Produto deletado com sucesso'}), 200

