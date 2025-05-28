# modules/transaction_manager.py

# Exemplo simples de dados de transação (em um cenário real, viria de uma fila, DB, Excel, etc.)
_transaction_data_list = [
    {"id": 1, "status": "PENDING", "retries": 0, "data": {"search_term": "BotCity RPA"}},
    {"id": 2, "status": "PENDING", "retries": 0, "data": {"search_term": "Python Automation"}},
    {"id": 3, "status": "PENDING", "retries": 0, "data": {"search_term": "REFramework Python"}},
    {"id": 4, "status": "PENDING", "retries": 0, "data": {"search_term": "Failed Item Test"}}, # Exemplo de item que pode falhar
]

def get_next_transaction_data(config):
    """
    Obtém o próximo item de transação pendente.
    Em um cenário real, isso interagiria com uma fila de orquestrador, DB, ou Excel.
    """
    for item in _transaction_data_list:
        if item["status"] == "PENDING" and item["retries"] < config["transaction_settings"]["max_retries"]:
            item["status"] = "IN_PROGRESS" # Marca como em progresso
            return item
    return None # Nenhum item pendente

def update_transaction_status(transaction_item, status, error_message=None):
    """
    Atualiza o status de um item de transação.
    """
    transaction_item["status"] = status
    if status == "FAILED":
        transaction_item["retries"] += 1
        transaction_item["error_message"] = error_message
        # Em um cenário real, você gravaria isso em um log ou DB
    elif status == "SUCCESS":
        transaction_item["error_message"] = None
    # O item já está em progresso, então não precisamos marcar "IN_PROGRESS" aqui

def process_item(bot, transaction_item, logger):
    """
    Lógica para processar um único item de transação.
    Você colocaria sua automação real aqui.
    """
    search_term = transaction_item["data"]["search_term"]
    logger.info(f"Processando item: {search_term}")

    try:
        # Exemplo de lógica: pesquisar no Google
        bot.browse(f"https://www.google.com/search?q={search_term}")
        bot.wait(3000)

        # Simulação de falha para testar o retry
        if "Failed Item Test" in search_term:
            raise Exception("Simulando falha no processamento!")

        # Adicione aqui sua lógica de automação para este item
        # Ex: Coletar dados, preencher formulário, etc.

        logger.info(f"Item '{search_term}' processado com sucesso.")
        return True # Sucesso
    except Exception as e:
        logger.error(f"Erro ao processar '{search_term}': {e}")
        return False # Falha