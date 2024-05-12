import logging

# Создаем логгер для jobs
jobs_logger = logging.getLogger('jobs')
jobs_logger.setLevel(logging.INFO)  # или любой другой уровень
jobs_handler = logging.FileHandler('logs/jobs.log')
jobs_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
jobs_logger.addHandler(jobs_handler)

# Создаем логгер для parser
parser_logger = logging.getLogger('parser')
parser_logger.setLevel(logging.INFO)  # или любой другой уровень
parser_handler = logging.FileHandler('logs/parser.log')
parser_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
parser_logger.addHandler(parser_handler)
