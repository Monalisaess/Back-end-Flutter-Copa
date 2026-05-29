"""Rotas HTTP de jogadores — delega a lógica para jogadores_service."""

from flask import Blueprint, jsonify, request

from app.services.jogadores_service import (
    atualizar_jogador,
    criar_jogador,
    listar_jogadores,
    remover_jogador,
)

jogadores_bp = Blueprint("jogadores", __name__)


# Flutter chama: GET /listajogadores  (query param opcional: ?idSelecao=1)
@jogadores_bp.route("/listajogadores", methods=["GET"])
def consulta_jogadores():
    id_selecao = request.args.get("idSelecao")
    return jsonify(listar_jogadores(id_selecao))


# Flutter chama: POST /cadastrajogador  →  body: {nomeJogador, posicaoJogador, idTimeFk}
@jogadores_bp.route("/cadastrajogador", methods=["POST"])
def create_jogador():
    return jsonify(criar_jogador(request.get_json() or {}))


# Flutter chama: PUT /atualizajogador  →  body: {idJogador, nomeJogador, posicaoJogador, idTimeFk}
@jogadores_bp.route("/atualizajogador", methods=["PUT"])
def update_jogador():
    return jsonify(atualizar_jogador(request.get_json() or {}))


# Flutter chama: DELETE /removejogador  →  body: {idJogador}
@jogadores_bp.route("/removejogador", methods=["DELETE"])
def delete_jogador():
    return jsonify(remover_jogador(request.get_json() or {}))
