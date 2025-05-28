# modules/utils.py
import yaml
import logging
import os
import sys

# --- Configuração de Logging ---
def setup_logger(log_folder="logs", log_file_name="robot.log"):
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), log_folder)
    os.makedirs(log_path, exist_ok=True) # Garante que a pasta de logs exista

    log_file = os.path.join(log_path, log_file_name)

    logger = logging.getLogger("REPyBot")
    logger.setLevel(logging.INFO)

    # Remove handlers existentes para evitar duplicação
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Handler para arquivo
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

# --- Leitura de Configuração ---
def read_config(config_path="config/config.yaml"):
    # Constrói o caminho completo a partir da raiz do projeto
    full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config_path)
    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        raise Exception(f"Arquivo de configuração não encontrado: {full_path}")
    except yaml.YAMLError as e:
        raise Exception(f"Erro ao parsear arquivo YAML: {e}")
    except Exception as e:
        raise Exception(f"Erro desconhecido ao ler a configuração: {e}")