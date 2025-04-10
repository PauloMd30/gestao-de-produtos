from routes import scheduler, notificar_produto_periodicamente, apagar_produtos_vencidos


# Adiciona os jobs
scheduler.add_job(notificar_produto_periodicamente, 'interval', hours=12)
scheduler.add_job(apagar_produtos_vencidos, 'interval', hours=12)

# Inicia o scheduler se ainda não estiver rodando
if not scheduler.running:
    scheduler.start()

