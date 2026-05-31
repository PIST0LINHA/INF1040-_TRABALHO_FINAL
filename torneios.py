import random


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
