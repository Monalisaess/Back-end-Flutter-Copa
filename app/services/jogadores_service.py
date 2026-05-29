"""Regras de negócio de jogadores (CRUD) — campos alinhados com o Flutter."""

from app.database.connection import conectaBanco


def listar_jogadores(id_selecao: str = None) -> list:
    """Retorna jogadores. Se id_selecao for passado, filtra por seleção.
    Flutter espera: idJogador, nomeJogador, posicaoJogador, idTimeFk, nomeSelecao.
    """
    bd = conectaBanco()
    cursor = bd.cursor()

    if id_selecao:
        sql = """SELECT j.id_jogador, j.nome, j.posicao, j.id_selecao_fk, s.nome
                 FROM jogador j
                 JOIN selecao s ON j.id_selecao_fk = s.id_selecao
                 WHERE j.id_selecao_fk = %s;"""
        cursor.execute(sql, (id_selecao,))
    else:
        sql = """SELECT j.id_jogador, j.nome, j.posicao, j.id_selecao_fk, s.nome
                 FROM jogador j
                 JOIN selecao s ON j.id_selecao_fk = s.id_selecao;"""
        cursor.execute(sql)

    resultado = cursor.fetchall()
    bd.close()

    return [
        {
            "idJogador": jog[0],        # Flutter usa idJogador
            "nomeJogador": jog[1],      # Flutter usa nomeJogador
            "posicaoJogador": jog[2],   # Flutter usa posicaoJogador
            "idTimeFk": jog[3],         # Flutter usa idTimeFk
            "nomeSelecao": jog[4],      # Flutter usa nomeSelecao
        }
        for jog in resultado
    ]


def criar_jogador(dados: dict) -> dict:
    """Cadastra um novo jogador.
    Flutter envia: nomeJogador, posicaoJogador, idTimeFk.
    """
    nome = dados.get("nomeJogador")
    posicao = dados.get("posicaoJogador")
    id_selecao = dados.get("idTimeFk")

    if not all([nome, posicao, id_selecao]):
        return {"mensagem": "Nome, posição e seleção são obrigatórios.", "code": 400}

    bd = conectaBanco()
    cursor = bd.cursor()
    cursor.execute(
        "INSERT INTO jogador (nome, posicao, id_selecao_fk) VALUES (%s, %s, %s);",
        (nome, posicao, id_selecao),
    )
    bd.commit()
    resultado = cursor.rowcount
    bd.close()

    if resultado > 0:
        return {"mensagem": "Jogador cadastrado com sucesso!", "code": 200}
    return {"mensagem": "Erro ao cadastrar jogador.", "code": 400}


def atualizar_jogador(dados: dict) -> dict:
    """Atualiza um jogador existente.
    Flutter envia: idJogador, nomeJogador, posicaoJogador, idTimeFk.
    """
    id_jogador = dados.get("idJogador")
    nome = dados.get("nomeJogador")
    posicao = dados.get("posicaoJogador")
    id_selecao = dados.get("idTimeFk")

    if not id_jogador:
        return {"mensagem": "ID do jogador é obrigatório.", "code": 400}

    bd = conectaBanco()
    cursor = bd.cursor()
    cursor.execute(
        "UPDATE jogador SET nome = %s, posicao = %s, id_selecao_fk = %s WHERE id_jogador = %s;",
        (nome, posicao, id_selecao, id_jogador),
    )
    bd.commit()
    resultado = cursor.rowcount
    bd.close()

    if resultado > 0:
        return {"mensagem": "Dados do jogador atualizados!", "code": 200}
    return {"mensagem": "Jogador não localizado ou sem alterações.", "code": 400}


def remover_jogador(dados: dict) -> dict:
    """Remove um jogador do banco.
    Flutter envia: idJogador.
    """
    id_jogador = dados.get("idJogador")

    if not id_jogador:
        return {"mensagem": "ID do jogador é obrigatório.", "code": 400}

    bd = conectaBanco()
    cursor = bd.cursor()
    cursor.execute("DELETE FROM jogador WHERE id_jogador = %s;", (id_jogador,))
    bd.commit()
    resultado = cursor.rowcount
    bd.close()

    if resultado > 0:
        return {"mensagem": "Jogador removido com sucesso!", "code": 200}
    return {"mensagem": "Jogador não localizado.", "code": 400}
