import json
import os

__all__ = ["inicializar", "criar_tabela", "atualizar_pontos", "ordenar_classificacao", "salvar"]

_ARQUIVO = os.path.join(os.path.dirname(__file__), "dados", "ranking_data.json")

_tabelas = {}  # {torneio_id: [lista de dicts]}


def _salvar() -> int:
    """Grava todas as tabelas de classificação no arquivo JSON.

    Requisito:
        Persistir rankings de torneios entre sessões da aplicação.

    Retorno:
        int: 0 sempre (erros de I/O propagam exceção).

    Pré-condições:
        - _ARQUIVO aponta para um caminho gravável.

    Pós-condições:
        - O arquivo JSON em _ARQUIVO reflete o estado atual de _tabelas.

    Restrições:
        Interna — não exposta via __all__. Chamada exclusivamente por salvar().

    Interface:
        nenhuma
    """
    with open(_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(_tabelas, f, ensure_ascii=False, indent=2)
    return 0


def _carregar() -> int:
    """Lê as tabelas de classificação do arquivo JSON e popula a variável de módulo.

    Requisito:
        Restaurar rankings ao iniciar a aplicação.

    Retorno:
        int: 0 se os dados foram carregados, 1 se o arquivo não existir.

    Pré-condições:
        - A variável global _tabelas está acessível.

    Pós-condições:
        - _tabelas contém os dados lidos (ou permanece {} se arquivo não existir).

    Restrições:
        Interna — não exposta via __all__. Chamada exclusivamente por inicializar().

    Interface:
        nenhuma
    """
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


def inicializar() -> int:
    """Carrega os dados persistidos de rankings do arquivo para a memória.

    Requisito:
        Permitir que o módulo de ranking esteja pronto para uso ao iniciar a aplicação.

    Retorno:
        int: 0 se os dados foram carregados com sucesso, 1 se o arquivo não existir.

    Pré-condições:
        - Deve ser chamada antes de qualquer outra função do módulo.

    Pós-condições:
        - O estado interno do módulo reflete os dados do arquivo (ou estado vazio).

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    return _carregar()


def criar_tabela(lista_times: list, torneio_id: str = "default") -> int:
    """Inicializa a tabela de classificação de um torneio com contadores zerados.

    Requisito:
        Preparar estrutura de dados de ranking ao criar um torneio.

    Parâmetros:
        lista_times (list): Lista de strings com os nomes dos times participantes.
                            Pode ser vazia (gera tabela vazia).
        torneio_id (str, opcional): Identificador do torneio. Padrão: "default".

    Retorno:
        int: 0 em caso de sucesso.

    Pré-condições:
        - lista_times é uma lista de strings (pode ser vazia).
        - torneio_id é uma string não vazia.

    Pós-condições:
        - _tabelas[torneio_id] contém uma entrada por time com todos os contadores = 0.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
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

    Requisito:
        Manter a classificação do torneio atualizada após cada partida registrada.

    Parâmetros:
        resultado (dict): Dict com as chaves obrigatórias:
                          time1 (str), time2 (str), gols_time1 (int), gols_time2 (int).
        torneio_id (str, opcional): Identificador do torneio. Padrão: "default".

    Retorno:
        int: 0 se ambos os times foram encontrados e atualizados.
             1 se a tabela do torneio não existir ou algum time não for encontrado.

    Pré-condições:
        - resultado contém as chaves time1, time2, gols_time1, gols_time2.
        - criar_tabela foi chamada com torneio_id antes desta função.

    Pós-condições:
        - Os registros de time1 e time2 em _tabelas[torneio_id] têm pontos,
          jogos, vitórias, empates, derrotas e saldo de gols atualizados.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    tabela = _tabelas.get(torneio_id)
    if tabela is None:
        return 1

    gols_casa = resultado["gols_time1"]
    gols_fora = resultado["gols_time2"]
    encontrado1 = False
    encontrado2 = False

    for time in tabela:
        if time["time"] == resultado["time1"]:
            encontrado1 = True
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
            encontrado2 = True
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

    return 0 if (encontrado1 and encontrado2) else 1


def ordenar_classificacao(torneio_id: str = "default") -> list:
    """Retorna a classificação de um torneio ordenada sem modificar a tabela original.

    Critérios de ordenação: pontos → vitórias → saldo de gols → gols marcados.

    Requisito:
        Exibir a classificação do torneio em ordem decrescente de desempenho.

    Parâmetros:
        torneio_id (str, opcional): Identificador do torneio. Padrão: "default".

    Retorno:
        list: Lista de dicts ordenada do primeiro ao último colocado;
              [] se o torneio não existir.

    Pré-condições:
        - nenhuma (retorna [] se torneio_id não existir em _tabelas).

    Pós-condições:
        - _tabelas permanece inalterado (operação de leitura com cópia ordenada).

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    tabela = _tabelas.get(torneio_id, [])
    return sorted(
        tabela,
        key=lambda t: (t["pontos"], t["vitorias"], t["saldo_gols"], t["gols_marcados"]),
        reverse=True,
    )


def salvar() -> int:
    """Persiste o estado atual de todos os rankings no arquivo de dados.

    Requisito:
        Garantir durabilidade dos dados de classificação entre sessões.

    Retorno:
        int: 0 em caso de sucesso; erros de I/O propagam exceção.

    Pré-condições:
        - _ARQUIVO aponta para um caminho gravável.

    Pós-condições:
        - O arquivo JSON reflete o estado atual de _tabelas.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    return _salvar()
