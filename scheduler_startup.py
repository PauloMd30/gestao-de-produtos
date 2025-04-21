from sched import scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from Database.models.produto import Produto
from whatsapp import enviar_mensagem_whatsapp
from dotenv import load_dotenv
import os   

load_dotenv()
numero_destino = os.environ.get('twilio_number2')
def apagar_produtos_vencidos():
    hoje = datetime.today().date()

    # Busca os produtos com data de validade anterior a hoje
    produtos_vencidos = Produto.objects(data_de_validade__lt=hoje)

    if produtos_vencidos:
        for produto in produtos_vencidos:
            print(f"[APAGADO] Produto {produto.nome} da marca {produto.marca} foi deletado.")
            produto.delete()
    else:
        print("[INFO] Nenhum produto vencido encontrado.")

    print(f"[LOG] Verificação de produtos vencidos executada em {hoje}")


def notificar_produto_periodicamente():
    hoje = datetime.today().date()
    data_limite = hoje + timedelta(days=7)

    # Busca produtos com validade próxima e que ainda não foram notificados
    produtos = Produto.objects(
        data_de_validade__lte=data_limite,
        notificado=False
    )

    mensagens_enviadas = []

    for produto in produtos:
        mensagem = f"O produto {produto.nome} da marca {produto.marca} tem validade próxima em {produto.data_de_validade.strftime('%d/%m/%Y')}."
        try:
            enviar_mensagem_whatsapp(mensagem, numero_destino)
            mensagens_enviadas.append(mensagem)
        except Exception as e:
            print(f"[ERRO] Erro ao enviar mensagem para {produto.nome}: {e}")

        # Marca como notificado
        produto.notificado = True
        produto.save()

    if mensagens_enviadas:
        for msg in mensagens_enviadas:
            print(f"[NOTIFICAÇÃO ENVIADA] {msg}")
    else:
        print("[INFO] Nenhum produto com validade próxima encontrado.")

    print(f"[LOG] Notificações enviadas em {hoje}")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(notificar_produto_periodicamente, 'interval', hours=24)
    scheduler.add_job(apagar_produtos_vencidos, 'interval', hours=24)
    scheduler.start()
    print("[INFO] Tarefas agendadas com sucesso.")
    print("[INFO] Scheduler iniciado.")