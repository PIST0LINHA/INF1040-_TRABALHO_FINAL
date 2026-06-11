import json
import os

__all__ = ["criar_tabela", "atualizar_pontos", "ordenar_classificacao", "mostrar_classificacao",
           "listar_torneios", "salvar"]

_ARQUIVO = os.path.join(os.path.dirname(__file__), "..", "dados", "ranking_data.json")

_tabelas = {}  # {torneio_id: [lista de dicts]}


def _salvar() -> int:
    with open(_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(_tabelas, f, ensure_ascii=False, indent=2)
    return 0


def _carregar() -> int:
    global _tabelas
    if not os.path.exists(_ARQUIVO):
        return 1
    with open(_ARQUIVO, "r", encoding="utf-8") as f:
        dados = json.load(f)
    # compatibilidade com formato antigo (lista plana)
    if isinstance(dados, list):
        _tabelas = {"default": dados}
    else:
        _tabelas = dados
    return 0


_carregar()


def criar_tabela(lista_times: list, torneio_id: str = "default") -> int:
    """Inicializa a tabela de classificação de um torneio com contadores zerados.

    Parâmetros:
        lista_times: list de strings com os nomes dos times participantes
        torneio_id: identificador do torneio (padrão: "default")

    Retorno:
        0 em caso de sucesso
    """
    _tabelas[torneio_id] = [
        {
            "time": time,
            "pontos": 0,
            "jogos": 0,
            "vitorias": 0,
            "empates": 0,
            "derrotas": 0,
            "gols_marcados": 0,
            "gols_sofridos": 0,
            "saldo_gols": 0,
        }
        for time in lista_times
    ]
    return 0


def atualizar_pontos(resultado: dict, torneio_id: str = "default") -> int:
    """Atualiza a tabela de classificação de um torneio com o resultado de uma partida.

    Vitória vale 3 pontos; empate vale 1 ponto; derrota vale 0 pontos.

    Parâmetros:
        resultado: dict com as chaves time1, time2, gols_time1, gols_time2
        torneio_id: identificador do torneio (padrão: "default")

    Retorno:
        0 se ambos os times foram encontrados na tabela
        1 se a tabela do torneio não existe ou algum time não foi encontrado
    """
    tabela = _tabelas.get(torneio_id)
    if tabela is None:
        return 1

    gols_casa = resultado["gols_time1"]
    gols_fora = resultado["gols_time2"]
    encontrado = False

    for time in tabela:
        if time["time"] == resultado["time1"]:
            encontrado = True
            time["jogos"] += 1
            time["gols_marcados"] += gols_casa
            time["gols_sofridos"] += gols_fora
            time["saldo_gols"] = time["gols_marcados"] - time["gols_sofridos"]
            if gols_casa > gols_fora:
                time["vitorias"] += 1
                time["pontos"] += 3
            elif gols_casa == gols_fora:
                time["empates"] += 1
                time["pontos"] += 1
            else:
                time["derrotas"] += 1
        elif time["time"] == resultado["time2"]:
            encontrado = True
            time["jogos"] += 1
            time["gols_marcados"] += gols_fora
            time["gols_sofridos"] += gols_casa
            time["saldo_gols"] = time["gols_marcados"] - time["gols_sofridos"]
            if gols_fora > gols_casa:
                time["vitorias"] += 1
                time["pontos"] += 3
            elif gols_fora == gols_casa:
                time["empates"] += 1
                time["pontos"] += 1
            else:
                time["derrotas"] += 1

    return 0 if encontrado else 1


def ordenar_classificacao(torneio_id: str = "default") -> list:
    """Retorna a classificação de um torneio ordenada sem modificar a tabela original.

    Critérios de ordenação: pontos → vitórias → saldo de gols → gols marcados.

    Parâmetros:
        torneio_id: identificador do torneio (padrão: "default")

    Retorno:
        list de dicts ordenada do primeiro ao último colocado; [] se torneio não existir
    """
    tabela = _tabelas.get(torneio_id, [])
    return sorted(
        tabela,
        key=lambda t: (t["pontos"], t["vitorias"], t["saldo_gols"], t["gols_marcados"]),
        reverse=True,
    )


def mostrar_classificacao(torneio_id: str = "default") -> int:
    """Exibe a tabela de classificação de um torneio formatada no terminal.

    Parâmetros:
        torneio_id: identificador do torneio (padrão: "default")

    Retorno:
        0 em caso de sucesso
        1 se a tabela estiver vazia ou não existir
    """
    tabela = _tabelas.get(torneio_id, [])
    if not tabela:
        return 1
    classificacao = ordenar_classificacao(torneio_id)
    cabecalho = f"{'Pos':<4} {'Time':<15} {'PTS':>4} {'J':>4} {'V':>4} {'E':>4} {'D':>4} {'GP':>4} {'GC':>4} {'SG':>4}"
    linhas = [cabecalho, "-" * len(cabecalho)]
    for pos, time in enumerate(classificacao, start=1):
        linhas.append(
            f"{pos:<4} {time['time']:<15} {time['pontos']:>4} {time['jogos']:>4} "
            f"{time['vitorias']:>4} {time['empates']:>4} {time['derrotas']:>4} "
            f"{time['gols_marcados']:>4} {time['gols_sofridos']:>4} {time['saldo_gols']:>4}"
        )
    print("\n".join(linhas))
    return 0


def listar_torneios() -> list:
    """Retorna a lista de IDs de torneios que possuem tabela de classificação.

    Retorno:
        list de strings com os IDs dos torneios
    """
    return list(_tabelas.keys())


def salvar() -> int:
    """Persiste o estado atual de todos os rankings no arquivo de dados.

    Retorno:
        0 em caso de sucesso
    """
    return _salvar()
