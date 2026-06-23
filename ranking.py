import json
import os

__all__ = ["inicializar", "criar_tabela", "atualizar_pontos", "ordenar_classificacao", "salvar"]

_ARQUIVO = os.path.join(os.path.dirname(__file__), "dados", "ranking_data.json")

_tabelas = {}  # {torneio_id: [lista de dicts]}


def _salvar() -> dict:
    """Grava todas as tabelas de classificação no arquivo JSON.

    Requisito:
        Persistir rankings de torneios entre sessões da aplicação.

    Retorno:
        dict: {status: 0, mensagem: "Rankings salvos.", dados: None}
              Erros de I/O propagam exceção.

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
    return {"status": 0, "mensagem": "Rankings salvos.", "dados": None}


def _carregar() -> dict:
    """Lê as tabelas de classificação do arquivo JSON e popula a variável de módulo.

    Requisito:
        Restaurar rankings ao iniciar a aplicação.

    Retorno:
        dict: {status: 0, mensagem: "Rankings carregados.", dados: None}
              se os dados foram carregados.
              {status: 1, mensagem: "Arquivo não encontrado.", dados: None}
              se o arquivo não existir.

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
        return {"status": 1, "mensagem": "Arquivo não encontrado.", "dados": None}
    with open(_ARQUIVO, "r", encoding="utf-8") as f:
        dados = json.load(f)
    if isinstance(dados, list):
        _tabelas = {"default": dados}
    else:
        _tabelas = dados
    return {"status": 0, "mensagem": "Rankings carregados.", "dados": None}


def inicializar() -> dict:
    """Carrega os dados persistidos de rankings do arquivo para a memória.

    Requisito:
        Permitir que o módulo de ranking esteja pronto para uso ao iniciar a aplicação.

    Retorno:
        dict: {status: 0, mensagem: "Dados de ranking carregados com sucesso.", dados: None}
              se os dados foram carregados com sucesso.
              {status: 1, mensagem: "Arquivo de ranking não encontrado...", dados: None}
              se o arquivo não existir (estado iniciado vazio).

    Pré-condições:
        - Deve ser chamada antes de qualquer outra função do módulo.

    Pós-condições:
        - O estado interno do módulo reflete os dados do arquivo (ou estado vazio).

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    if _carregar()["status"] == 0:
        return {"status": 0, "mensagem": "Dados de ranking carregados com sucesso.", "dados": None}
    return {"status": 1, "mensagem": "Arquivo de ranking não encontrado. Estado iniciado vazio.", "dados": None}


def criar_tabela(lista_times: list, torneio_id: str = "default") -> dict:
    """Inicializa a tabela de classificação de um torneio com contadores zerados.

    Requisito:
        Preparar estrutura de dados de ranking ao criar um torneio.

    Parâmetros:
        lista_times (list): Lista de strings com os nomes dos times participantes.
                            Pode ser vazia (gera tabela vazia).
        torneio_id (str, opcional): Identificador do torneio. Padrão: "default".

    Retorno:
        dict: {status: 0, mensagem: "Tabela criada com N time(s).", dados: None}
              em caso de sucesso.
              {status: 1, mensagem: "Erro: ...", dados: None}
              se torneio_id for vazio ou lista_times não for uma lista.

    Pré-condições:
        - lista_times é uma lista de strings (pode ser vazia).
        - torneio_id é uma string não vazia.

    Pós-condições:
        - Em caso de sucesso (status 0), _tabelas[torneio_id] contém uma entrada
          por time com todos os contadores zerados.
        - Em caso de erro (status 1), _tabelas permanece inalterado.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    if not torneio_id or not isinstance(lista_times, list):
        return {"status": 1, "mensagem": "Erro: torneio_id não pode ser vazio e lista_times deve ser uma lista.", "dados": None}
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
    return {"status": 0, "mensagem": f"Tabela criada com {len(lista_times)} time(s).", "dados": None}


def atualizar_pontos(resultado: dict, torneio_id: str = "default") -> dict:
    """Atualiza a tabela de classificação de um torneio com o resultado de uma partida.

    Vitória vale 3 pontos; empate vale 1 ponto; derrota vale 0 pontos.

    Requisito:
        Manter a classificação do torneio atualizada após cada partida registrada.

    Parâmetros:
        resultado (dict): Dict com as chaves obrigatórias:
                          time1 (str), time2 (str), gols_time1 (int), gols_time2 (int).
        torneio_id (str, opcional): Identificador do torneio. Padrão: "default".

    Retorno:
        dict: {status: 0, mensagem: "Pontuação atualizada com sucesso.", dados: None}
              se ambos os times foram encontrados e atualizados.
              {status: 1, mensagem: "Erro: ...", dados: None}
              se a tabela do torneio não existir ou algum time não for encontrado.

    Pré-condições:
        - resultado contém as chaves time1, time2, gols_time1, gols_time2.
        - criar_tabela foi chamada com torneio_id antes desta função.

    Pós-condições:
        - Em caso de sucesso (status 0), os registros de time1 e time2 em
          _tabelas[torneio_id] têm pontos, jogos, vitórias, empates, derrotas
          e saldo de gols atualizados.
        - Em caso de erro (status 1), _tabelas permanece inalterado.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    tabela = _tabelas.get(torneio_id)
    if tabela is None:
        return {"status": 1, "mensagem": f"Erro: tabela do torneio '{torneio_id}' não encontrada.", "dados": None}

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

    if encontrado1 and encontrado2:
        return {"status": 0, "mensagem": "Pontuação atualizada com sucesso.", "dados": None}
    return {"status": 1, "mensagem": "Erro: um ou mais times não foram encontrados na tabela.", "dados": None}


def ordenar_classificacao(torneio_id: str = "default") -> dict:
    """Retorna a classificação de um torneio ordenada sem modificar a tabela original.

    Critérios de ordenação: pontos → vitórias → saldo de gols → gols marcados.

    Requisito:
        Exibir a classificação do torneio em ordem decrescente de desempenho.

    Parâmetros:
        torneio_id (str, opcional): Identificador do torneio. Padrão: "default".

    Retorno:
        dict: {status: 0, mensagem: "Classificação com N time(s).",
               dados: [lista de dicts ordenada do primeiro ao último colocado]}
              Dados é [] se o torneio existir mas não tiver times cadastrados.
              {status: 1, mensagem: "Erro: torneio '...' não encontrado.", dados: None}
              se o torneio_id não existir em _tabelas.

    Pré-condições:
        - nenhuma.

    Pós-condições:
        - _tabelas permanece inalterado (operação de leitura com cópia ordenada).

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    if torneio_id not in _tabelas:
        return {"status": 1, "mensagem": f"Erro: torneio '{torneio_id}' não encontrado.", "dados": None}
    tabela = _tabelas[torneio_id]
    ordenada = sorted(
        tabela,
        key=lambda t: (t["pontos"], t["vitorias"], t["saldo_gols"], t["gols_marcados"]),
        reverse=True,
    )
    return {"status": 0, "mensagem": f"Classificação com {len(ordenada)} time(s).", "dados": ordenada}


def salvar() -> dict:
    """Persiste o estado atual de todos os rankings no arquivo de dados.

    Requisito:
        Garantir durabilidade dos dados de classificação entre sessões.

    Retorno:
        dict: {status: 0, mensagem: "Rankings salvos com sucesso.", dados: None}
              Erros de I/O propagam exceção.

    Pré-condições:
        - _ARQUIVO aponta para um caminho gravável.

    Pós-condições:
        - O arquivo JSON reflete o estado atual de _tabelas.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    _salvar()
    return {"status": 0, "mensagem": "Rankings salvos com sucesso.", "dados": None}
