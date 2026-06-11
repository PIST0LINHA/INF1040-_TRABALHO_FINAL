import json
import os

__all__ = ["registrar", "listar", "por_rodada", "rodadas", "resetar", "salvar"]

_ARQUIVO = os.path.join(os.path.dirname(__file__), "..", "dados", "partidas_data.json")

_lista = []


def _salvar() -> int:
    with open(_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(_lista, f, ensure_ascii=False, indent=2)
    return 0


def _carregar() -> int:
    global _lista
    if not os.path.exists(_ARQUIVO):
        return 1
    with open(_ARQUIVO, "r", encoding="utf-8") as f:
        _lista = json.load(f)
    return 0


_carregar()


def registrar(time1: str, time2: str, gols1: int, gols2: int, rodada=None, torneio_id=None) -> dict:
    """Valida e registra o resultado de uma partida.

    Parâmetros:
        time1: nome do primeiro time
        time2: nome do segundo time
        gols1: gols marcados pelo time1 (>= 0)
        gols2: gols marcados pelo time2 (>= 0)
        rodada: número da rodada do torneio, ou None se partida avulsa
        torneio_id: ID do torneio ao qual a partida pertence (opcional)

    Retorno:
        dict com os dados da partida em caso de sucesso
        str com mensagem de erro em caso de falha
    """
    if not time1 or not time2:
        return "Erro: nomes dos times não podem ser vazios."
    if time1 == time2:
        return "Erro: um time não pode disputar contra si mesmo."
    if rodada is not None:
        for p in _lista:
            if p.get("rodada") == rodada and p.get("torneio_id") == torneio_id:
                if (p["time1"] == time1 and p["time2"] == time2) or \
                   (p["time1"] == time2 and p["time2"] == time1):
                    return f"Partida {time1} × {time2} já foi registrada nesta rodada."
    nova = {"time1": time1, "time2": time2, "gols_time1": gols1, "gols_time2": gols2}
    if rodada is not None:
        nova["rodada"] = rodada
    if torneio_id is not None:
        nova["torneio_id"] = torneio_id
    _lista.append(nova)
    return nova


def listar(filtro_time=None, filtro_rodada=None, torneio_id=None) -> list:
    """Retorna partidas registradas com filtros opcionais.

    Parâmetros:
        filtro_time: nome do time para filtrar (opcional)
        filtro_rodada: número da rodada para filtrar (opcional)
        torneio_id: ID do torneio para filtrar (opcional)

    Retorno:
        list de dicts com as partidas que atendem ao filtro
    """
    resultado = list(_lista)
    if torneio_id is not None:
        resultado = [p for p in resultado if p.get("torneio_id") == torneio_id]
    if filtro_time:
        resultado = [
            p for p in resultado
            if p.get("time1", "").lower() == filtro_time.lower()
            or p.get("time2", "").lower() == filtro_time.lower()
        ]
    if filtro_rodada:
        resultado = [
            p for p in resultado
            if str(p.get("rodada", "")) == str(filtro_rodada)
        ]
    return resultado


def por_rodada(rodada, torneio_id=None) -> list:
    """Retorna todas as partidas de uma rodada específica.

    Parâmetros:
        rodada: número da rodada
        torneio_id: ID do torneio para filtrar (opcional)

    Retorno:
        list de dicts com as partidas da rodada; [] se não houver nenhuma
    """
    resultado = [p for p in _lista if p.get("rodada") == rodada]
    if torneio_id is not None:
        resultado = [p for p in resultado if p.get("torneio_id") == torneio_id]
    return resultado


def rodadas(torneio_id=None) -> list:
    """Retorna a lista ordenada das rodadas que possuem partidas registradas.

    Parâmetros:
        torneio_id: ID do torneio para filtrar (opcional)

    Retorno:
        list de strings com os números das rodadas em ordem crescente
    """
    fonte = _lista if torneio_id is None else [p for p in _lista if p.get("torneio_id") == torneio_id]
    return sorted({str(p.get("rodada")) for p in fonte if p.get("rodada")})


def resetar(torneio_id=None) -> int:
    """Remove partidas da memória.

    Parâmetros:
        torneio_id: se fornecido, remove apenas as partidas desse torneio;
                    se None, remove todas as partidas

    Retorno:
        0 em caso de sucesso
    """
    global _lista
    if torneio_id is not None:
        _lista = [p for p in _lista if p.get("torneio_id") != torneio_id]
    else:
        _lista.clear()
    return 0


def salvar() -> int:
    """Persiste o estado atual das partidas no arquivo de dados.

    Retorno:
        0 em caso de sucesso
    """
    return _salvar()
