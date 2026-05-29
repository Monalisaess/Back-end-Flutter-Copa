"""Rotas HTTP de partidas — delega a lógica para partidas_service."""

from flask import Blueprint, jsonify, request

from app.services.partidas_service import (
    atualizar_partida,
    criar_partida,
    listar_partidas,
    remover_partida,
)

partidas_bp = Blueprint("partidas", __name__)


# Flutter chama: GET /listapartidas
@partidas_bp.route("/listapartidas", methods=["GET"])
def consulta_partidas():
    return jsonify(listar_partidas())


# Flutter chama: POST /cadastrapartida  →  body: {dataPartida, placarEquipeCasa,
#                                                  placarEquipeVisitante, idEquipeCasa, idEquipeVisitante}
@partidas_bp.route("/cadastrapartida", methods=["POST"])
def create_partida():
    return jsonify(criar_partida(request.get_json() or {}))


# Flutter chama: PUT /atualizapartida  →  body: {idPartida, dataPartida, placarEquipeCasa,
#                                                 placarEquipeVisitante, idEquipeCasa, idEquipeVisitante}
@partidas_bp.route("/atualizapartida", methods=["PUT"])
def update_partida():
    return jsonify(atualizar_partida(request.get_json() or {}))


# Flutter chama: DELETE /removepartida  →  body: {idPartida}
@partidas_bp.route("/removepartida", methods=["DELETE"])
def delete_partida():
    return jsonify(remover_partida(request.get_json() or {}))
