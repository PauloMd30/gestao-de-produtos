from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()
numero_destino = os.environ.get('twilio_number2')  # Número de destino no formato internacional (incluindo o código do país)

# Função para enviar a mensagem via WhatsApp
def enviar_mensagem_whatsapp(mensagem, numero_destino):
    # Configurações da conta Twilio
    account_sid = os.environ.get('account_sid')
    auth_token = os.environ.get('auth_token')
    twilio_whatsapp_number = os.environ.get('twilio_number')

    # Verifica se as credenciais foram fornecidas
    if not account_sid or not auth_token or not twilio_whatsapp_number:
        raise ValueError("As credenciais da Twilio não estão configuradas corretamente nas variáveis de ambiente.")
    
    # Cria um cliente Twilio
    client = Client(account_sid, auth_token)

    try:
        # Envia a mensagem via WhatsApp
        message = client.messages.create(
            body=mensagem,
            from_=f'whatsapp:{twilio_whatsapp_number}',
            to=f'whatsapp:{numero_destino}'
        )

        # Log da resposta da API Twilio
        print(f"Mensagem enviada com sucesso! SID: {message.sid}")
        return message.sid

    except Exception as e:
        # Se ocorrer um erro, vamos logar o erro
        print(f"Erro ao enviar a mensagem: {e}")
        raise  # Relançar o erro para que o código continue tratando-o
