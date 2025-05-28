# modules/app_interactions.py
# Este módulo conteria funções para interações comuns com aplicações/navegadores

def init_applications(bot, config, logger):
    """
    Inicializa as aplicações necessárias para o robô.
    """
    logger.info("Inicializando aplicações...")
    # Exemplo: Lógica para abrir navegador ou aplicativo desktop
    # Se o bot já estiver aberto, pode reusá-lo ou fechar e abrir novamente.
    try:
        if isinstance(bot, type(bot)('')): # Gambiarra para verificar o tipo sem instanciar
             # Se for WebBot, já foi instanciado no main, então só navega ou verifica
            logger.info(f"Navegando para URL inicial: {config['app_settings']['url_google']}")
            bot.browse(config['app_settings']['url_google'])
        # Exemplo Desktop:
        # bot.browse("caminho/para/seu/aplicativo.exe")
        logger.info("Aplicações inicializadas com sucesso.")
        return True
    except Exception as e:
        logger.error(f"Erro ao inicializar aplicações: {e}")
        raise # Re-lança o erro para ser capturado no main

def login_application(bot, config, logger):
    """
    Realiza o login em uma aplicação.
    """
    logger.info("Realizando login na aplicação...")
    # Lógica de login aqui (ex: preencher campos de usuário/senha, clicar em botão)
    try:
        # Exemplo: bot.find_element("username_field", By.ID).send_keys(config["credentials"]["user_name"])
        # bot.find_element("password_field", By.ID).send_keys(config["credentials"]["password"])
        # bot.find_element("login_button", By.ID).click()
        logger.info("Login realizado com sucesso.")
        return True
    except Exception as e:
        logger.error(f"Erro ao realizar login: {e}")
        raise

def close_applications(bot, logger):
    """
    Fecha todas as aplicações abertas pelo robô.
    """
    logger.info("Fechando aplicações...")
    try:
        if isinstance(bot, type(bot)('')) and bot._driver: # Verifica se é WebBot e se o driver está ativo
            bot.stop_browser()
            logger.info("Navegador fechado.")
        # Exemplo Desktop:
        # bot.stop_process("nome_do_seu_aplicativo.exe")
        logger.info("Aplicações fechadas com sucesso.")
        return True
    except Exception as e:
        logger.error(f"Erro ao fechar aplicações: {e}")
        raise