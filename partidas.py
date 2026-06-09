import random
import json
import os

ARQ_LISTA_PARTIDAS = "partidas.json"
_lista_partidas = []


def carregar_partidas() -> int:
    global _lista_partidas
    if os.path.exists(ARQ_LISTA_PARTIDAS):
        with open(ARQ_LISTA_PARTIDAS, "r", encoding="utf-8") as f:
            _lista_partidas = json.load(f)
            return 0
    else:
        _lista_partidas = []
        return 1


# sempre retorna 0
def salvar_partidas() -> int:
    with open(ARQ_LISTA_PARTIDAS, "w", encoding="utf-8") as f:
        json.dump(_lista_partidas, f, ensure_ascii=False, indent=2)
        return 0


def simular_partida(time1: str, time2: str) -> dict:
    if not time1 or not time2:
        _lista_partidas.append({"erro": "Erro: nomes dos times não podem ser vazio"})
        return {"erro": "Erro: nomes dos times não podem ser vazios"}

    if time1 == time2:
        _lista_partidas.append(
            {"erro": "Erro: um time não pode disputar contra si mesmo"}
        )
        return {"erro": "Erro: um time não pode disputar contra si mesmo"}

    partida = {
        "time1": time1,
        "time2": time2,
        "gols_time1": random.randint(0, 5),
        "gols_time2": random.randint(0, 5),
    }

    _lista_partidas.append(partida)
    return partida


def gerar_resultado(partida: dict) -> str:
    if "erro" in partida:
        print(f"{partida['erro']}")
        return f"{partida['erro']}"

    return (
        f"{partida['time1']}:{partida['gols_time1']}  x"
        f"{partida['time2']}: {partida['gols_time2']}"
    )


def registrar_resultado(
    lista_partidas: list, time1: str, time2: str, gols_time1: int, gols_time2: int
) -> dict:
    if not time1 or not time2:
        _lista_partidas.append({"erro": "Erro: nomes dos times não podem ser vazios"})
        return {"erro": "Erro: nomes dos times não podem ser vazios"}

    if time1 == time2:
        _lista_partidas.append(
            {"erro": "Erro: um time não pode disputar contra si mesmo"}
        )
        return {"erro": "Erro: um time não pode disputar contra si mesmo"}

    partida = {
        "time1": time1,
        "time2": time2,
        "gols_time1": gols_time1,
        "gols_time2": gols_time2,
    }

    lista_partidas.append(partida)
    return partida


def listar_partidas(_lista_partidas: list) -> list:
    return _lista_partidas.copy()
