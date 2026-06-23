import json
import os

__all__ = ["inicializar", "registrar", "listar", "por_rodada", "rodadas", "resetar", "salvar"]

_ARQUIVO = os.path.join(os.path.dirname(__file__), "dados", "partidas_data.json")

_lista = []


def _salvar() -> dict:
    """Grava o estado atual da lista de partidas no arquivo JSON.

    Requisito:
        Persistir resultados de partidas entre sessões da aplicação.

    Retorno:
        dict: {status: 0, mensagem: "Partidas salvas.", dados: None}
              Erros de I/O propagam exceção.

    Pré-condições:
        - _ARQUIVO aponta para um caminho gravável.

    Pós-condições:
        - O arquivo JSON em _ARQUIVO contém todas as partidas de _lista.

    Restrições:
        Interna — não exposta via __all__. Chamada exclusivamente por salvar().

    Interface:
        nenhuma
    """
    with open(_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(_lista, f, ensure_ascii=False, indent=2)
    return {"status": 0, "mensagem": "Partidas salvas.", "dados": None}


def _carregar() -> dict:
    """Lê a lista de partidas do arquivo JSON e popula a variável de módulo.

    Requisito:
        Restaurar resultados de partidas ao iniciar a aplicação.

    Retorno:
        dict: {status: 0, mensagem: "Partidas carregadas.", dados: None}
              se os dados foram carregados.
              {status: 1, mensagem: "Arquivo não encontrado.", dados: None}
              se o arquivo não existir.

    Pré-condições:
        - A variável global _lista está acessível.

    Pós-condições:
        - _lista contém as partidas lidas do arquivo (ou permanece [] se não existir).

    Restrições:
        Interna — não exposta via __all__. Chamada exclusivamente por inicializar().

    Interface:
        nenhuma
    """
    global _lista
    if not os.path.exists(_ARQUIVO):
        return {"status": 1, "mensagem": "Arquivo não encontrado.", "dados": None}
    with open(_ARQUIVO, "r", encoding="utf-8") as f:
        _lista = json.load(f)
    return {"status": 0, "mensagem": "Partidas carregadas.", "dados": None}


def inicializar() -> dict:
    """Carrega os dados persistidos de partidas do arquivo para a memória.

    Requisito:
        Permitir que o módulo de partidas esteja pronto para uso ao iniciar a aplicação.

    Retorno:
        dict: {status: 0, mensagem: "Dados de partidas carregados com sucesso.", dados: None}
              se os dados foram carregados com sucesso.
              {status: 1, mensagem: "Arquivo de partidas não encontrado...", dados: None}
              se o arquivo não existir (estado iniciado vazio).

    Pré-condições:
        - Deve ser chamada antes de qualquer outra função do módulo.

    Pós-condições:
        - O estado interno do módulo reflete os dados do arquivo (ou lista vazia).

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    if _carregar()["status"] == 0:
        return {"status": 0, "mensagem": "Dados de partidas carregados com sucesso.", "dados": None}
    return {"status": 1, "mensagem": "Arquivo de partidas não encontrado. Estado iniciado vazio.", "dados": None}


def registrar(time1: str, time2: str, gols1: int, gols2: int, rodada=None, torneio_id=None) -> dict:
    """Valida e registra o resultado de uma partida na lista interna.

    Requisito:
        Registrar resultados de partidas garantindo integridade
        (sem duplicatas na mesma rodada/torneio e sem time contra si mesmo).

    Parâmetros:
        time1 (str): Nome do primeiro time. Não pode ser vazio.
        time2 (str): Nome do segundo time. Não pode ser igual a time1.
        gols1 (int): Gols marcados pelo time1. Deve ser >= 0.
        gols2 (int): Gols marcados pelo time2. Deve ser >= 0.
        rodada (int, opcional): Número da rodada. Padrão: None (partida avulsa).
        torneio_id (str, opcional): ID do torneio. Padrão: None.

    Retorno:
        dict: {status: 0, mensagem: "Partida registrada com sucesso.",
               dados: {time1, time2, gols_time1, gols_time2[, rodada][, torneio_id]}}
              em caso de sucesso.
              {status: 1, mensagem: "Erro: ...", dados: None}
              se validação falhar ou partida já registrada na rodada.

    Pré-condições:
        - time1 e time2 são strings não vazias e distintas.
        - gols1 e gols2 são inteiros >= 0.

    Pós-condições:
        - Em caso de sucesso (status 0), a partida é adicionada a _lista.
        - Em caso de erro (status 1), _lista permanece inalterada.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    if not time1 or not time2:
        return {"status": 1, "mensagem": "Erro: nomes dos times não podem ser vazios.", "dados": None}
    if time1 == time2:
        return {"status": 1, "mensagem": "Erro: um time não pode disputar contra si mesmo.", "dados": None}
    if rodada is not None:
        for p in _lista:
            if p.get("rodada") == rodada and p.get("torneio_id") == torneio_id:
                if (p["time1"] == time1 and p["time2"] == time2) or \
                   (p["time1"] == time2 and p["time2"] == time1):
                    return {"status": 1, "mensagem": f"Partida {time1} × {time2} já foi registrada nesta rodada.", "dados": None}
    nova = {"time1": time1, "time2": time2, "gols_time1": gols1, "gols_time2": gols2}
    if rodada is not None:
        nova["rodada"] = rodada
    if torneio_id is not None:
        nova["torneio_id"] = torneio_id
    _lista.append(nova)
    return {"status": 0, "mensagem": "Partida registrada com sucesso.", "dados": nova}


def listar(filtro_time=None, filtro_rodada=None, torneio_id=None) -> dict:
    """Retorna as partidas registradas, com filtros opcionais.

    Requisito:
        Permitir consulta e filtragem de partidas por time, rodada e/ou torneio.

    Parâmetros:
        filtro_time (str, opcional): Nome do time para filtrar. Padrão: None (sem filtro).
        filtro_rodada (str|int, opcional): Número da rodada. Padrão: None (sem filtro).
        torneio_id (str, opcional): ID do torneio. Padrão: None (sem filtro).

    Retorno:
        dict: {status: 0, mensagem: "N partida(s) encontrada(s).",
               dados: [lista de dicts com as partidas que atendem aos filtros]}
              Dados é sempre uma lista; [] se nenhuma partida atender aos filtros.

    Pré-condições:
        - Filtros, quando fornecidos, são valores comparáveis aos armazenados.

    Pós-condições:
        - _lista permanece inalterada.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
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
    return {"status": 0, "mensagem": f"{len(resultado)} partida(s) encontrada(s).", "dados": resultado}


def por_rodada(rodada, torneio_id=None) -> dict:
    """Retorna todas as partidas de uma rodada específica.

    Requisito:
        Permitir consulta de resultados de uma rodada para avançar fases do torneio.

    Parâmetros:
        rodada (int): Número da rodada a consultar.
        torneio_id (str, opcional): ID do torneio para filtrar. Padrão: None.

    Retorno:
        dict: {status: 0, mensagem: "N partida(s) na rodada X.",
               dados: [lista de dicts com as partidas da rodada]}
              Dados é sempre uma lista; [] se não houver partidas nessa rodada.

    Pré-condições:
        - rodada é um valor compatível com o campo "rodada" das partidas.

    Pós-condições:
        - _lista permanece inalterada.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    resultado = [p for p in _lista if p.get("rodada") == rodada]
    if torneio_id is not None:
        resultado = [p for p in resultado if p.get("torneio_id") == torneio_id]
    return {"status": 0, "mensagem": f"{len(resultado)} partida(s) na rodada {rodada}.", "dados": resultado}


def rodadas(torneio_id=None) -> dict:
    """Retorna lista ordenada das rodadas que possuem ao menos uma partida registrada.

    Requisito:
        Permitir navegação e filtragem de partidas por rodada.

    Parâmetros:
        torneio_id (str, opcional): ID do torneio para filtrar. Padrão: None.

    Retorno:
        dict: {status: 0, mensagem: "N rodada(s) encontrada(s).",
               dados: [lista de strings com os números de rodada em ordem crescente]}
              Dados é sempre uma lista; [] se não houver rodadas.

    Pré-condições:
        - nenhuma.

    Pós-condições:
        - _lista permanece inalterada.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    fonte = _lista if torneio_id is None else [p for p in _lista if p.get("torneio_id") == torneio_id]
    resultado = sorted({str(p.get("rodada")) for p in fonte if p.get("rodada")})
    return {"status": 0, "mensagem": f"{len(resultado)} rodada(s) encontrada(s).", "dados": resultado}


def resetar(torneio_id=None) -> dict:
    """Remove partidas da memória, total ou parcialmente por torneio.

    Requisito:
        Permitir reinício de torneio descartando resultados registrados.

    Parâmetros:
        torneio_id (str, opcional): Se fornecido, remove apenas partidas desse torneio.
                                    Se None, remove todas as partidas. Padrão: None.

    Retorno:
        dict: {status: 0, mensagem: "Partidas removidas com sucesso.", dados: None}

    Pré-condições:
        - nenhuma.

    Pós-condições:
        - Se torneio_id fornecido: partidas com esse torneio_id são removidas de _lista.
        - Se torneio_id None: _lista fica vazia.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    global _lista
    if torneio_id is not None:
        _lista = [p for p in _lista if p.get("torneio_id") != torneio_id]
    else:
        _lista.clear()
    return {"status": 0, "mensagem": "Partidas removidas com sucesso.", "dados": None}


def salvar() -> dict:
    """Persiste o estado atual das partidas no arquivo de dados.

    Requisito:
        Garantir durabilidade dos resultados de partidas entre sessões.

    Retorno:
        dict: {status: 0, mensagem: "Partidas salvas com sucesso.", dados: None}
              Erros de I/O propagam exceção.

    Pré-condições:
        - _ARQUIVO aponta para um caminho gravável.

    Pós-condições:
        - O arquivo JSON reflete o estado atual de _lista.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    _salvar()
    return {"status": 0, "mensagem": "Partidas salvas com sucesso.", "dados": None}
