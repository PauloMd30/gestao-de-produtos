from flask import Blueprint, render_template, request
from datetime import datetime, timedelta, date
from Database import Produto  # Certifique-se de importar o modelo Produto
from bson.objectid import ObjectId  # Import ObjectId para conversão


route_produto = Blueprint("produto", __name__)
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
    data = request.json
    # Verifique o formato da data
    try:
        data_de_validade = datetime.strptime(data["data validade"], '%d/%m/%Y').date()
    except ValueError:
        # Caso a data esteja no formato 'YYYY-MM-DD', converta para o formato correto
        data_de_validade = datetime.strptime(data["data validade"], '%Y-%m-%d').date()
    
    novo_produto = Produto(
        nome=data["nome"],
        marca=data["marca"],
        codigo_de_barras=data["codigo de barras"],
        data_de_validade=data_de_validade
    )
    novo_produto.save()
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

