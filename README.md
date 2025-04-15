Sistema de Gestão de Produtos com Notificações via WhatsApp
Esta aplicação foi desenvolvida com Python (Flask) e tem como objetivo gerenciar produtos com base em sua validade, oferecendo funcionalidades automatizadas de controle e notificação.

🚀 Funcionalidades principais:
Cadastro, edição, listagem e exclusão de produtos com campos como nome, marca, código de barras e data de validade.

Interface web integrada usando templates Jinja2 para interação com o sistema.

Validação automática de datas no backend para garantir integridade dos dados.

Consulta de produtos com validade próxima (até 7 dias) para facilitar o controle de estoque.

Exclusão automática de produtos vencidos com verificações diárias agendadas (via APScheduler).

Integração com WhatsApp (Twilio) para envio de mensagens automáticas notificando sobre produtos com vencimento próximo.

Banco de dados MongoDB utilizando MongoEngine como ORM para modelagem dos dados.

🔧 Tecnologias utilizadas:
Python + Flask

MongoDB + MongoEngine

Twilio API (WhatsApp Messaging)

APScheduler (tarefas agendadas)

HTML/Jinja2 (renderização de templates)

dotenv (para variáveis de ambiente)

💡 Destaques técnicos:
Modularização com Blueprints no Flask para organização das rotas.

Agendamento de tarefas em segundo plano sem depender de cron externo.

Utilização de ObjectId para operações seguras com documentos MongoDB.

Manipulação de datas com datetime e timedelta para lógica de validade.

Integração com WhatsApp totalmente automatizada para alertas de vencimento.

