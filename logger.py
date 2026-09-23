import logging
import os

# Cria o diretório de log se não existir
log_dir = os.path.join(os.path.dirname(__file__), 'log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configuração do logger da aplicação
logger = logging.getLogger('petgrid_logger')
logger.setLevel(logging.INFO)

log_path = os.path.join(log_dir, 'app.log')
file_handler = logging.FileHandler(log_path, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
