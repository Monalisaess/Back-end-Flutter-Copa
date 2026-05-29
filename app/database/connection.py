"""Conexão com o MySQL — lê as credenciais do arquivo .env."""

import os

import pymysql
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (cada dev tem o seu com sua senha)
load_dotenv()


def conectaBanco():
    """Retorna uma conexão aberta com o banco MySQL.

    As credenciais são lidas do .env:
        DB_NAME   → nome do banco (padrão: copado_mundo)
        DB_HOST   → endereço do servidor (padrão: localhost)
        DB_USER   → usuário MySQL (padrão: root)
        DB_PASSWORD → senha do MySQL (obrigatório definir no .env)
        DB_PORT   → porta (padrão: 3306)
    """
    return pymysql.connect(
        database=os.getenv("DB_NAME", "copado_mundo"),
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        passwd=os.getenv("DB_PASSWORD", ""),
        port=int(os.getenv("DB_PORT", 3306)),
        charset="utf8mb4",
    )
