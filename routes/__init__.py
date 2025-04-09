from flask import Blueprint, render_template

route_home = Blueprint("home", __name__)

@route_home.route("/")
def home():
     return render_template("index.html")


from flask import Blueprint, render_template, request
from datetime import datetime, timedelta, date
from Database import Produto  # Certifique-se de importar o modelo Produto
from bson.objectid import ObjectId  # Import ObjectId para conversão
from whatsapp import enviar_mensagem_whatsapp
from apscheduler.schedulers.background import BackgroundScheduler


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


def apagar_produtos_vencidos():
    hoje = datetime.today().date()  # Obtém a data atual
    
    # Usando MongoEngine para buscar os produtos vencidos
    produtos_vencidos = Produto.objects(data_de_validade__lt=hoje)  # Seleciona os produtos com data de validade anterior à de hoje

    # Verifica se há produtos vencidos
    if produtos_vencidos:
        for produto in produtos_vencidos:
            produto.delete()  # Deleta o produto
            print(f"Produto {produto.nome} da marca {produto.marca} foi deletado, pois já estava vencido.")
    else:
        print("Nenhum produto vencido encontrado.")

    print(f"Produtos vencidos verificados e apagados em {hoje}")

def notificar_produto_periodicamente():
    hoje = datetime.today().date()
    data_limite = hoje + timedelta(days=7)
    
    # Selecionando os produtos com validade próxima e que ainda não foram notificados
    produtos = Produto.objects(
        data_de_validade__lte=data_limite,  # Validade próxima
        notificado=False  # Produtos que ainda não foram notificados
    )
    
    mensagens_enviadas = []  # Lista para armazenar as mensagens enviadas
    
    # Processa todos os produtos selecionados
    for produto in produtos:
        mensagem = f"O produto {produto.nome} da marca {produto.marca} tem validade próxima em {produto.data_de_validade.strftime('%d/%m/%Y')}."
        
        try:
            # Envia a mensagem via WhatsApp
            enviar_mensagem_whatsapp(mensagem, "+5511957165078")  # Substitua pelo número de destino desejado
            mensagens_enviadas.append(mensagem)  # Armazena a mensagem enviada
        except Exception as e:
            # Log de erro caso a mensagem não seja enviada
            print(f"Erro ao enviar mensagem para o produto {produto.nome}: {e}")
        
        # Marca o produto como notificado
        produto.notificado = True
        produto.save()  # Salva a atualização no banco

    # Verifica se houve mensagens enviadas e imprime
    if mensagens_enviadas:
        for msg in mensagens_enviadas:
            print(f"Mensagem enviada: {msg}")
    else:
        print("Nenhum produto com validade próxima encontrado.")

    # Log final indicando o dia em que as notificações foram enviadas
    print(f"Notificações enviadas em {hoje}")


# Configuração do APScheduler para rodar a cada 24 horas
scheduler = BackgroundScheduler()
scheduler.add_job(notificar_produto_periodicamente, 'interval', hours=24) # Ajuste o intervalo conforme necessário
scheduler.add_job(apagar_produtos_vencidos, 'interval', hours=24)  
if not scheduler.running:
    scheduler.start()


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

