# main.py
from botcity.core import DesktopBot
from botcity.web import WebBot, Browser

# Importar os módulos da sua arquitetura
from modules.utils import setup_logger, read_config
from modules.transaction_manager import get_next_transaction_data, update_transaction_status, process_item
from modules.app_interactions import init_applications, close_applications, login_application

import sys
import os
import time # Para simular waits


def main():
    # --- Configuração Inicial ---
    # 1. Configurar o logger
    logger = setup_logger()
    logger.info("Robô REPyBot iniciado!")

    # 2. Carregar as configurações
    config = None
    try:
        config = read_config()
        logger.info("Configurações carregadas com sucesso.")
    except Exception as e:
        logger.critical(f"Erro CRÍTICO ao carregar configurações: {e}. Encerrando o robô.", exc_info=True)
        sys.exit(1) # Encerrar o programa

    # 3. Inicializar o Bot (WebBot ou DesktopBot)
    # Pode ser instanciado no Init ou Globalmente, dependendo da necessidade
    bot = None
    current_transaction_item = None
    system_exception = False # Flag para indicar exceção no sistema (global)
    success_count = 0
    failed_count = 0

    # --- Lógica da Máquina de Estados ---
    state = "INIT"
    while True:
        try:
            if state == "INIT":
                logger.info("Estado: INIT - Iniciando as aplicações...")
                bot = WebBot() # Instanciar o bot aqui
                bot.driver_path = config["app_settings"]["driver_path"] # Pega o caminho do driver da config
                bot.headless = False # Para ver o navegador abrindo

                if init_applications(bot, config, logger):
                    # login_application(bot, config, logger) # Descomente se precisar de login
                    state = "GET_TRANSACTION_DATA"
                else:
                    raise Exception("Falha na inicialização das aplicações.")

            elif state == "GET_TRANSACTION_DATA":
                logger.info("Estado: GET_TRANSACTION_DATA - Obtendo próxima transação...")
                current_transaction_item = get_next_transaction_data(config)

                if current_transaction_item:
                    logger.info(f"Transação '{current_transaction_item['id']}' obtida. Status: {current_transaction_item['status']}")
                    state = "PROCESS_TRANSACTION"
                else:
                    logger.info("Nenhuma transação pendente encontrada. Indo para o estado de finalização.")
                    state = "END_PROCESS"

            elif state == "PROCESS_TRANSACTION":
                logger.info(f"Estado: PROCESS_TRANSACTION - Processando transação '{current_transaction_item['id']}'...")
                if process_item(bot, current_transaction_item, logger):
                    update_transaction_status(current_transaction_item, "SUCCESS")
                    logger.info(f"Transação '{current_transaction_item['id']}' processada com SUCESSO.")
                    success_count += 1
                else:
                    # Se process_item retornar False, significa que a lógica de negócio falhou
                    raise Exception(f"Falha na lógica de processamento para transação '{current_transaction_item['id']}'.")

                state = "GET_TRANSACTION_DATA" # Volta para buscar a próxima transação

            elif state == "END_PROCESS":
                logger.info("Estado: END_PROCESS - Finalizando o robô...")
                close_applications(bot, logger)
                logger.info(f"Robô finalizado. Transações processadas com sucesso: {success_count}. Falhas: {failed_count}.")
                break # Sai do loop principal

        except Exception as e:
            logger.error(f"Exceção no estado '{state}' para transação '{current_transaction_item['id'] if current_transaction_item else 'N/A'}': {e}", exc_info=True)

            if state == "PROCESS_TRANSACTION" and current_transaction_item:
                update_transaction_status(current_transaction_item, "FAILED", str(e))
                failed_count += 1
                # Implementar lógica de retry (ex: se current_transaction_item['retries'] < max_retries)
                if current_transaction_item['retries'] < config["transaction_settings"]["max_retries"]:
                    logger.warning(f"Tentando novamente a transação '{current_transaction_item['id']}'. Tentativa: {current_transaction_item['retries']}/{config['transaction_settings']['max_retries']}")
                    # Volta para processar o mesmo item, pois o status foi atualizado
                    state = "PROCESS_TRANSACTION" # Tentar processar novamente
                else:
                    logger.error(f"Transação '{current_transaction_item['id']}' falhou após {config['transaction_settings']['max_retries']} tentativas.")
                    state = "GET_TRANSACTION_DATA" # Vai para a próxima transação
            else:
                # Erro em INIT ou GET_TRANSACTION_DATA (ou outro estado crítico)
                logger.critical(f"Erro crítico irrecuperável no estado '{state}'. Encerrando o robô.", exc_info=True)
                system_exception = True
                break # Sai do loop principal

        # Pequeno delay para evitar loop excessivo em caso de bugs
        time.sleep(1)

    # --- Limpeza Final (em caso de exceção) ---
    if system_exception:
        logger.error("Robô terminou com exceção de sistema.")
        if bot and bot._driver:
            try:
                bot.stop_browser()
                logger.info("Navegador forçadamente fechado após exceção de sistema.")
            except Exception as e:
                logger.error(f"Erro ao tentar fechar navegador após exceção: {e}")
        sys.exit(1) # Sair com código de erro

    logger.info("Robô REPyBot concluído com sucesso (ou com tratamento de exceções).")