"""Regras de negÃ³cio de seleÃ§Ãµes (CRUD) â€” campos alinhados com o Flutter."""

import pymysql

from app.database.connection import conectaBanco


def listar_selecoes() -> list:
    """Retorna todas as seleÃ§Ãµes.
    Flutter espera: idTime, nome, cidade (cidade = grupo no banco).
    """
    bd = conectaBanco()
    cursor = bd.cursor()
    cursor.execute("SELECT id_selecao, nome, grupo FROM selecao;")
    resultado = cursor.fetchall()
    bd.close()

    return [
        {
            "idTime": sel[0],       # Flutter usa idTime
            "nome": sel[1],         # Flutter usa nome
            "cidade": sel[2],       # Flutter usa cidade (mapeado para grupo no banco)
        }
        for sel in resultado
    ]


def criar_selecao(dados: dict) -> dict:
    """Cadastra uma nova seleÃ§Ã£o.
    Flutter envia: nomeEquipe, cidadeEquipe.
    """
    nome = dados.get("nomeEquipe")
    grupo = dados.get("cidadeEquipe")

    if not all([nome, grupo]):
        return {"mensagem": "Nome e cidade/grupo sÃ£o obrigatÃ³rios.", "code": 400}

    bd = conectaBanco()
    cursor = bd.cursor()
    cursor.execute(
        "INSERT INTO selecao (nome, grupo) VALUES (%s, %s);",
        (nome, grupo),
    )
    bd.commit()
    resultado = cursor.rowcount
    bd.close()

    if resultado > 0:
        return {"mensagem": "SeleÃ§Ã£o cadastrada com sucesso!", "code": 200}
    return {"mensagem": "Erro ao cadastrar seleÃ§Ã£o.", "code": 400}


def atualizar_selecao(dados: dict) -> dict:
    """Atualiza uma seleÃ§Ã£o existente.
    Flutter envia: idEquipe, nomeEquipe, cidadeEquipe.
    """
    id_selecao = dados.get("idEquipe")
    nome = dados.get("nomeEquipe")
    grupo = dados.get("cidadeEquipe")

    if not id_selecao:
        return {"mensagem": "ID da seleÃ§Ã£o Ã© obrigatÃ³rio.", "code": 400}

    bd = conectaBanco()
    cursor = bd.cursor()
    cursor.execute(
        "UPDATE selecao SET nome = %s, grupo = %s WHERE id_selecao = %s;",
        (nome, grupo, id_selecao),
    )
    bd.commit()
    resultado = cursor.rowcount
    bd.close()

    if resultado > 0:
        return {"mensagem": "SeleÃ§Ã£o atualizada com sucesso!", "code": 200}
    return {"mensagem": "SeleÃ§Ã£o nÃ£o localizada ou sem alteraÃ§Ãµes.", "code": 400}


def remover_selecao(dados: dict) -> dict:
    """Remove uma selecao do banco.
    Flutter envia: idEquipe.
    """
    id_selecao = dados.get("idEquipe")

    if not id_selecao:
        return {"mensagem": "ID da selecao e obrigatorio.", "code": 400}

    bd = conectaBanco()
    cursor = bd.cursor()
    try:
        cursor.execute("DELETE FROM selecao WHERE id_selecao = %s;", (id_selecao,))
        bd.commit()
        resultado = cursor.rowcount
    except pymysql.err.IntegrityError:
        bd.rollback()
        return {
            "mensagem": "Nao e possivel remover esta selecao porque existem jogadores ou partidas vinculadas.",
            "code": 400,
        }
    finally:
        bd.close()

    if resultado > 0:
        return {"mensagem": "Selecao removida com sucesso!", "code": 200}
    return {"mensagem": "Selecao nao localizada.", "code": 400}
