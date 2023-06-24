import os
from logging.config import fileConfig
from os import environ
from alembic import context

from config import path_to_env
from models import Address_table
from dotenv import load_dotenv

# Alembic Config объект предоставляет доступ
# к переменным из файла alembic.ini
load_dotenv(path_to_env)
config = context.config

section = config.config_ini_section
config.set_section_option(section, "DB_USER", os.getenv("DB_USER"))
config.set_section_option(section, "DB_PASS", os.getenv("DB_PASS"))
config.set_section_option(section, "DB_NAME", os.getenv("DB_NAME"))
config.set_section_option(section, "DB_HOST", os.getenv("DB_HOST"))

fileConfig(config.config_file_name)

target_metadata = [Address_table.metadata]