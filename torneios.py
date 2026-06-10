import random
import json
import os

ARQ_LISTA_PARTIDAS = "partidas.json"
_partidas_estipuladas = []


def carregar_partidas() -> int:
    global _partidas_estipuladas
    if os.path.exists(ARQ_LISTA_PARTIDAS):
        with open(ARQ_LISTA_PARTIDAS, "r", encoding="utf-8") as f:
            _partidas_estipuladas = json.load(f)
            return 0
    else:
        _partidas_estipuladas = []
        return 1


def buscar_partida_estipulada(time1, time2):
    for partida in _partidas_estipuladas:
        if "erro" in partida:
            continue
        if partida.get("time1") == time1 and partida.get("time2") == time2:
            return {
                "time1": time1,
                "time2": time2,
                "gols_time1": partida["gols_time1"],
                "gols_time2": partida["gols_time2"],
            }
        if partida.get("time1") == time2 and partida.get("time2") == time1:
            return {
                "time1": time1,
                "time2": time2,
                "gols_time1": partida["gols_time2"],
                "gols_time2": partida["gols_time1"],
            }
    return None


def gerar_confronto(lista_times):
    embaralhados = list(lista_times)
    random.shuffle(embaralhados)
    confrontos = []
    for i in range(0, len(embaralhados) - 1, 2):
        confrontos.append((embaralhados[i], embaralhados[i + 1]))
    return confrontos


def iniciar_rodada(confrontos):
    resultados = []
    for time1, time2 in confrontos:
        resultados.append({
            "time1": time1,
            "time2": time2,
            "gols_time1": random.randint(0, 5),
            "gols_time2": random.randint(0, 5),
        })
    return resultados


def avancar_fase(resultados):
    classificados = []
    for partida in resultados:
        gols1 = partida["gols_time1"]
        gols2 = partida["gols_time2"]
        if gols1 > gols2:
            classificados.append(partida["time1"])
        elif gols2 > gols1:
            classificados.append(partida["time2"])
        else:
            classificados.append(partida["time1"])
            classificados.append(partida["time2"])
    return classificados
