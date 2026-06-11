import random
import json
import os
from . import partidas

__all__ = [
    "criar", "listar", "get_ativo", "set_ativo",
    "get_confrontos", "get_rodada", "get_campeao",
    "confrontos_pendentes", "rodada_completa", "avancar", "resetar_ativo", "salvar",
    "gerar_confronto", "iniciar_rodada", "avancar_fase",
]

_ARQUIVO = os.path.join(os.path.dirname(__file__), "..", "dados", "torneio_data.json")

_torneios = []
_proximo_id = 1
_torneio_ativo_id = None


def _salvar() -> int:
    dados = {
        "torneios": [
            {**t, "confrontos": [list(c) for c in t["confrontos"]]}
            for t in _torneios
        ],
        "proximo_id": _proximo_id,
        "torneio_ativo_id": _torneio_ativo_id,
    }
    with open(_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    return 0


def _carregar() -> int:
    global _torneios, _proximo_id, _torneio_ativo_id
    if not os.path.exists(_ARQUIVO):
        return 1
    with open(_ARQUIVO, "r", encoding="utf-8") as f:
        dados = json.load(f)
    _torneios = [
        {**t, "confrontos": [tuple(c) for c in t.get("confrontos", [])]}
        for t in dados.get("torneios", [])
    ]
    _proximo_id = dados.get("proximo_id", 1)
    _torneio_ativo_id = dados.get("torneio_ativo_id", None)
    return 0


_carregar()


def _get_torneio(torneio_id):
    for t in _torneios:
        if t["id"] == torneio_id:
            return t
    return None


# --- Estado do torneio ---

def criar(nome: str, nomes_times: list) -> dict:
    """Cria um novo torneio e o define como ativo.

    Parâmetros:
        nome: nome do torneio (se vazio, recebe nome padrão)
        nomes_times: lista de nomes dos times participantes (par, >= 2)

    Retorno:
        dict com os dados do torneio criado
    """
    global _proximo_id, _torneio_ativo_id
    torneio_id = str(_proximo_id)
    torneio = {
        "id": torneio_id,
        "nome": nome.strip() if nome.strip() else f"Torneio {_proximo_id}",
        "times": nomes_times,
        "rodada": 1,
        "campeao": None,
        "confrontos": gerar_confronto(nomes_times),
    }
    _proximo_id += 1
    _torneios.append(torneio)
    _torneio_ativo_id = torneio_id
    return torneio


def listar() -> list:
    """Retorna todos os torneios criados.

    Retorno:
        list de dicts com os dados de cada torneio
    """
    return list(_torneios)


def get_ativo():
    """Retorna o torneio atualmente ativo.

    Retorno:
        dict com os dados do torneio ativo, ou None se não houver
    """
    return _get_torneio(_torneio_ativo_id)


def set_ativo(torneio_id: str) -> int:
    """Define o torneio ativo pelo ID.

    Parâmetros:
        torneio_id: ID do torneio a ativar

    Retorno:
        0 em caso de sucesso, 1 se o torneio não for encontrado
    """
    global _torneio_ativo_id
    if _get_torneio(torneio_id) is None:
        return 1
    _torneio_ativo_id = torneio_id
    return 0


def get_confrontos() -> list:
    """Retorna os confrontos da rodada atual do torneio ativo.

    Retorno:
        list de tuplas (time1, time2), ou [] se não houver torneio ativo
    """
    t = get_ativo()
    return list(t["confrontos"]) if t else []


def get_rodada() -> int:
    """Retorna o número da rodada atual do torneio ativo.

    Retorno:
        int com o número da rodada (0 se não houver torneio ativo)
    """
    t = get_ativo()
    return t["rodada"] if t else 0


def get_campeao():
    """Retorna o campeão do torneio ativo se encerrado.

    Retorno:
        str com o nome do campeão, ou None
    """
    t = get_ativo()
    return t["campeao"] if t else None


def confrontos_pendentes() -> list:
    """Retorna os confrontos da rodada atual do torneio ativo sem resultado registrado.

    Retorno:
        list de tuplas (time1, time2) dos confrontos pendentes
    """
    t = get_ativo()
    if not t:
        return []
    registradas = partidas.por_rodada(t["rodada"], torneio_id=t["id"])
    pendentes = []
    for c in t["confrontos"]:
        tem = any(
            (p["time1"] == c[0] and p["time2"] == c[1]) or
            (p["time1"] == c[1] and p["time2"] == c[0])
            for p in registradas
        )
        if not tem:
            pendentes.append(c)
    return pendentes


def rodada_completa() -> bool:
    """Verifica se todos os confrontos da rodada atual têm resultado registrado.

    Retorno:
        True se a rodada está completa, False caso contrário
    """
    t = get_ativo()
    if not t:
        return False
    return len(t["confrontos"]) > 0 and len(confrontos_pendentes()) == 0


def avancar() -> int:
    """Avança para a próxima fase ou define o campeão se restar apenas um time.

    Retorno:
        0 em caso de sucesso, 1 se não houver torneio ativo
    """
    t = get_ativo()
    if not t:
        return 1
    resultados = partidas.por_rodada(t["rodada"], torneio_id=t["id"])
    classificados = avancar_fase(resultados)
    if len(classificados) == 1:
        t["campeao"] = classificados[0]
        t["confrontos"] = []
    else:
        t["rodada"] += 1
        t["confrontos"] = gerar_confronto(classificados)
    return 0


def resetar_ativo() -> int:
    """Reinicia o torneio ativo do zero com os mesmos times.

    Retorno:
        0 em caso de sucesso, 1 se não houver torneio ativo
    """
    t = get_ativo()
    if not t:
        return 1
    t["rodada"] = 1
    t["campeao"] = None
    t["confrontos"] = gerar_confronto(t["times"])
    return 0


def salvar() -> int:
    """Persiste o estado de todos os torneios no arquivo de dados.

    Retorno:
        0 em caso de sucesso
    """
    return _salvar()


# --- Funções puras ---

def gerar_confronto(lista_times: list) -> list:
    """Gera pares de confronto aleatórios a partir de uma lista de times.

    Parâmetros:
        lista_times: lista de nomes dos times

    Retorno:
        list de tuplas (time1, time2) com os pares gerados
    """
    embaralhados = list(lista_times)
    random.shuffle(embaralhados)
    confrontos = []
    for i in range(0, len(embaralhados) - 1, 2):
        confrontos.append((embaralhados[i], embaralhados[i + 1]))
    return confrontos


def iniciar_rodada(confrontos: list) -> list:
    """Simula resultados aleatórios para todos os confrontos de uma rodada.

    Parâmetros:
        confrontos: list de tuplas (time1, time2)

    Retorno:
        list de dicts com time1, time2, gols_time1, gols_time2
    """
    return [
        {
            "time1": time1,
            "time2": time2,
            "gols_time1": random.randint(0, 5),
            "gols_time2": random.randint(0, 5),
        }
        for time1, time2 in confrontos
    ]


def avancar_fase(resultados: list) -> list:
    """Determina os times classificados para a próxima fase.

    Em caso de empate, ambos os times avançam.

    Parâmetros:
        resultados: list de dicts com time1, time2, gols_time1, gols_time2

    Retorno:
        list de strings com os nomes dos times classificados
    """
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
