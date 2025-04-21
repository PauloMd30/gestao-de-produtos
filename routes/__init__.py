from flask import Blueprint, render_template

route_home = Blueprint("home", __name__)

@route_home.route("/")
def home():
     return render_template("index.html")

import os
from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, timedelta, date
from Database import Produto  
from bson.objectid import ObjectId  # Import ObjectId para conversão
from whatsapp import enviar_mensagem_whatsapp
from apscheduler.schedulers.background import BackgroundScheduler
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

    # Sucesso: retorna HTML renderizado
    return render_template('item_produto.html', produto=novo_produto)

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
    produto = Produto.objects.get(id=ObjectId(produto_id))
    produto.data_de_validade = produto.data_de_validade.strftime('%d/%m/%Y')
    return render_template('form_produto.html', produto=produto)

@route_produto.route('/<string:produto_id>/update', methods=['PUT'])
def atualizar_produto(produto_id):
    data = request.json
    produto_editado = Produto.objects.get(id=ObjectId(produto_id))
    produto_editado.nome = data['nome']
    produto_editado.marca = data['marca']
    produto_editado.codigo_de_barras = data['codigo de barras']
    
    # Verifique o formato da data
    try:
        produto_editado.data_de_validade = datetime.strptime(data['data validade'], '%d/%m/%Y').date()
    except ValueError:
        # Caso a data esteja no formato 'YYYY-MM-DD', converta para o formato correto
        produto_editado.data_de_validade = datetime.strptime(data['data validade'], '%Y-%m-%d').date()
    
    produto_editado.save()
    return render_template('item_produto.html', produto=produto_editado)
# apaga um produto
@route_produto.route("/<string:produto_id>/delete", methods=["DELETE"])
def deletar_produto(produto_id):
    produto = Produto.objects.get(id=ObjectId(produto_id))
    produto.delete()
    return 'produto deletado com sucesso'

