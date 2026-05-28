import random
import json

ARQ_LISTA_PARTIDAS = "partidas.json"
_lista_partidas = []
lista_partidas = []

def simular_partida(time1:str, time2:str) -> int:
    if not time1 or not time2:
        return{"erro": "Erro: nomes dos timer não podem ser vazio"}

    if time1 == time2:
        return{"erro": "Erro: um time não pode disputar contra si mesmo"}

    partida = {
        "time1": time1,
        "time2": time2,
        "gols_time1": random.randint(0, 5),
        "gols_time2": random.randint(0, 5)
    }
    
    _lista_partidas.append(partida)
    return 1


def gerar_resultado(partida:dict) -> int:
    if "erro" in partida:
        print(f'{partida["erro"]}')
        return -1
    print(
        f'{partida["time1"]}:{partida["gols_time1"]}  x'
        f'{partida["time2"]}: {partida["gols_time2"]}'
    )
    return 1


def registrar_resultado(lista_partidas:list, time1:str, time2:str, gols_time1:str, gols_time2:str) -> dict:
    if not time1 or not time2:
        return{"erro": "Erro: nomes dos times não podem ser vazios"}

    if time1 == time2:
        return{"erro": "Erro: um time não pode disputar contra si mesmo"}

    partida = {
        "time1": time1,
        "time2": time2,
        "gols_time1": gols_time1,
        "gols_time2": gols_time2
    }

    lista_partidas.append(partida)
    return partida


def listar_partidas(lista_partidas:list) -> list:
    return lista_partidas.copy()
