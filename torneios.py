import random
import json
import os
import partidas

__all__ = [
    "inicializar", "criar", "listar", "get_ativo", "set_ativo", "desativar",
    "confrontos_pendentes", "avancar", "resetar_ativo", "resetar", "salvar",
    "contexto_partida",
]

_ARQUIVO = os.path.join(os.path.dirname(__file__), "dados", "torneio_data.json")

_torneios = []
_proximo_id = 1
_torneio_ativo_id = None


def _salvar() -> int:
    """Grava o estado completo de todos os torneios no arquivo JSON.

    Requisito:
        Persistir dados de torneios entre sessões da aplicação.

    Retorno:
        int: 0 sempre (erros de I/O propagam exceção).

    Pré-condições:
        - _ARQUIVO aponta para um caminho gravável.

    Pós-condições:
        - O arquivo JSON em _ARQUIVO reflete o estado atual de _torneios,
          _proximo_id e _torneio_ativo_id.

    Restrições:
        Interna — não exposta via __all__. Chamada por salvar() e desativar().

    Interface:
        nenhuma
    """
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
    """Lê os dados de torneios do arquivo JSON e popula as variáveis de módulo.

    Requisito:
        Restaurar estado de torneios ao iniciar a aplicação.

    Retorno:
        int: 0 se os dados foram carregados, 1 se o arquivo não existir.

    Pré-condições:
        - As variáveis globais _torneios, _proximo_id e _torneio_ativo_id estão acessíveis.

    Pós-condições:
        - _torneios contém os torneios lidos (com confrontos como tuplas).
        - _proximo_id e _torneio_ativo_id refletem os valores persistidos.

    Restrições:
        Interna — não exposta via __all__. Chamada exclusivamente por inicializar().

    Interface:
        nenhuma
    """
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


def _get_torneio(torneio_id):
    """Localiza um torneio na lista interna pelo seu ID.

    Parâmetros:
        torneio_id (str): ID do torneio a localizar.

    Retorno:
        dict: Dados do torneio se encontrado, None caso contrário.

    Restrições:
        Interna — não exposta via __all__.

    Interface:
        nenhuma
    """
    for t in _torneios:
        if t["id"] == torneio_id:
            return t
    return None


def _eh_confronto_ativo(time1: str, time2: str) -> bool:
    """Verifica se dois times formam um confronto da rodada atual do torneio ativo.

    Parâmetros:
        time1 (str): Nome do primeiro time.
        time2 (str): Nome do segundo time.

    Retorno:
        bool: True se o par forma um confronto da rodada atual; False caso contrário.

    Pré-condições:
        - time1 e time2 são strings não vazias.

    Pós-condições:
        - O torneio ativo permanece inalterado.

    Restrições:
        Interna — não exposta via __all__.

    Interface:
        nenhuma
    """
    t = _get_torneio(_torneio_ativo_id)
    return any(
        (c[0] == time1 and c[1] == time2) or (c[1] == time1 and c[0] == time2)
        for c in (t["confrontos"] if t else [])
    )


def _gerar_confronto(lista_times: list) -> list:
    """Gera pares de confronto aleatórios a partir de uma lista de times.

    Parâmetros:
        lista_times (list): Lista de strings com nomes dos times.
                            Deve ter número par de elementos.

    Retorno:
        list: Lista de tuplas (time1, time2) com os pares gerados aleatoriamente.

    Pré-condições:
        - len(lista_times) >= 2 e len(lista_times) % 2 == 0.

    Pós-condições:
        - Cada time aparece exatamente uma vez nos confrontos.

    Restrições:
        Interna — não exposta via __all__.

    Interface:
        nenhuma
    """
    embaralhados = list(lista_times)
    random.shuffle(embaralhados)
    confrontos = []
    for i in range(0, len(embaralhados) - 1, 2):
        confrontos.append((embaralhados[i], embaralhados[i + 1]))
    return confrontos


def _avancar_fase(resultados: list) -> list:
    """Determina os times classificados para a próxima fase com base nos resultados.

    Em caso de empate, ambos os times avançam.

    Parâmetros:
        resultados (list): Lista de dicts com as chaves:
                           time1, time2, gols_time1, gols_time2.

    Retorno:
        list: Lista de strings com os nomes dos times classificados.

    Pré-condições:
        - resultados é uma lista de dicts com as chaves obrigatórias acima.

    Pós-condições:
        - Cada partida contribui com 1 (vitória/derrota) ou 2 (empate) times
          na lista retornada.

    Restrições:
        Interna — não exposta via __all__.

    Interface:
        nenhuma
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


def inicializar() -> dict:
    """Carrega os dados persistidos de torneios do arquivo para a memória.

    Requisito:
        Permitir que o módulo de torneios esteja pronto para uso ao iniciar a aplicação.

    Retorno:
        dict: {status: 0, mensagem: "Dados de torneios carregados com sucesso.", dados: None}
              se os dados foram carregados com sucesso.
              {status: 1, mensagem: "Arquivo de torneios não encontrado...", dados: None}
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
    if _carregar() == 0:
        return {"status": 0, "mensagem": "Dados de torneios carregados com sucesso.", "dados": None}
    return {"status": 1, "mensagem": "Arquivo de torneios não encontrado. Estado iniciado vazio.", "dados": None}


def criar(nome: str, nomes_times: list) -> dict:
    """Cria um novo torneio com eliminação simples e o define como ativo.

    Requisito:
        Criar torneio com número par de times (>= 2) e nome único, gerando
        os confrontos da primeira rodada aleatoriamente.

    Parâmetros:
        nome (str): Nome do torneio. Se vazio, recebe nome padrão "Torneio N".
        nomes_times (list): Lista de strings com nomes dos times participantes.
                            Deve ter número par de elementos e pelo menos 2.

    Retorno:
        dict: {status: 0, mensagem: "Torneio '...' criado com sucesso.",
               dados: {id, nome, times, rodada, campeao, confrontos}}
              em caso de sucesso.
              {status: 1, mensagem: "Erro: ...", dados: None}
              se a lista tiver número ímpar, menos de 2 times ou nome duplicado.

    Pré-condições:
        - nomes_times é uma lista com len >= 2 e len % 2 == 0.

    Pós-condições:
        - Em caso de sucesso (status 0), o torneio é adicionado a _torneios
          com rodada=1 e campeao=None, e _torneio_ativo_id aponta para ele.
        - Em caso de erro (status 1), _torneios permanece inalterado.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    global _proximo_id, _torneio_ativo_id
    if len(nomes_times) < 2:
        return {"status": 1, "mensagem": "Erro: o torneio requer ao menos 2 times.", "dados": None}
    if len(nomes_times) % 2 != 0:
        return {"status": 1, "mensagem": "Erro: o número de times deve ser par.", "dados": None}
    nome_final = nome.strip() if nome.strip() else f"Torneio {_proximo_id}"
    if any(t["nome"].lower() == nome_final.lower() for t in _torneios):
        return {"status": 1, "mensagem": f"Erro: já existe um torneio com o nome \"{nome_final}\". Escolha outro nome.", "dados": None}
    torneio_id = str(_proximo_id)
    torneio = {
        "id": torneio_id,
        "nome": nome_final,
        "times": nomes_times,
        "rodada": 1,
        "campeao": None,
        "confrontos": _gerar_confronto(nomes_times),
    }
    _proximo_id += 1
    _torneios.append(torneio)
    _torneio_ativo_id = torneio_id
    return {"status": 0, "mensagem": f"Torneio '{nome_final}' criado com sucesso.", "dados": torneio}


def listar() -> dict:
    """Retorna todos os torneios criados.

    Requisito:
        Permitir visualização de todos os torneios cadastrados.

    Retorno:
        dict: {status: 0, mensagem: "N torneio(s) encontrado(s).",
               dados: [lista de dicts com os dados de cada torneio]}
              Dados é sempre uma lista; [] se não houver torneios.

    Pré-condições:
        - nenhuma.

    Pós-condições:
        - _torneios permanece inalterado (retorna cópia rasa da lista).

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    copia = list(_torneios)
    return {"status": 0, "mensagem": f"{len(copia)} torneio(s) encontrado(s).", "dados": copia}


def get_ativo() -> dict:
    """Retorna os dados do torneio atualmente ativo.

    Requisito:
        Permitir que outras partes da aplicação consultem o torneio em andamento.

    Retorno:
        dict: {status: 0, mensagem: "Torneio ativo: '...'.",
               dados: {id, nome, times, rodada, campeao, confrontos}}
              se houver torneio ativo.
              {status: 1, mensagem: "Nenhum torneio ativo no momento.", dados: None}
              se não houver torneio ativo.

    Pré-condições:
        - nenhuma.

    Pós-condições:
        - _torneios e _torneio_ativo_id permanecem inalterados.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    t = _get_torneio(_torneio_ativo_id)
    if t is not None:
        return {"status": 0, "mensagem": f"Torneio ativo: '{t['nome']}'.", "dados": t}
    return {"status": 1, "mensagem": "Nenhum torneio ativo no momento.", "dados": None}


def set_ativo(torneio_id: str) -> dict:
    """Define o torneio ativo pelo ID.

    Requisito:
        Permitir ativação de um torneio existente para retomar ou iniciar operações.

    Parâmetros:
        torneio_id (str): ID do torneio a ser definido como ativo.

    Retorno:
        dict: {status: 0, mensagem: "Torneio '...' definido como ativo.", dados: None}
              em caso de sucesso.
              {status: 1, mensagem: "Erro: torneio com ID '...' não encontrado.", dados: None}
              se o torneio com o ID fornecido não existir.

    Pré-condições:
        - torneio_id é uma string correspondente a um torneio existente.

    Pós-condições:
        - Em caso de sucesso (status 0), _torneio_ativo_id é igual a torneio_id.
        - Em caso de erro (status 1), _torneio_ativo_id permanece inalterado.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    global _torneio_ativo_id
    if _get_torneio(torneio_id) is None:
        return {"status": 1, "mensagem": f"Erro: torneio com ID '{torneio_id}' não encontrado.", "dados": None}
    _torneio_ativo_id = torneio_id
    return {"status": 0, "mensagem": f"Torneio '{torneio_id}' definido como ativo.", "dados": None}


def desativar() -> dict:
    """Remove o torneio ativo sem apagar seus dados da lista.

    Requisito:
        Encerrar o estado ativo de um torneio sem excluir seu histórico.

    Retorno:
        dict: {status: 0, mensagem: "Torneio desativado com sucesso.", dados: None}
              em caso de sucesso.
              {status: 1, mensagem: "Não há torneio ativo para desativar.", dados: None}
              se não houver torneio ativo.

    Pré-condições:
        - nenhuma.

    Pós-condições:
        - Em caso de sucesso (status 0), _torneio_ativo_id é None e os dados
          do torneio permanecem em _torneios; o arquivo de dados é atualizado.
        - Em caso de erro (status 1), o estado permanece inalterado.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    global _torneio_ativo_id
    if _torneio_ativo_id is None:
        return {"status": 1, "mensagem": "Não há torneio ativo para desativar.", "dados": None}
    _torneio_ativo_id = None
    _salvar()
    return {"status": 0, "mensagem": "Torneio desativado com sucesso.", "dados": None}


def confrontos_pendentes() -> dict:
    """Retorna os confrontos da rodada atual sem resultado registrado.

    Requisito:
        Indicar quais partidas ainda precisam ter resultado registrado para
        que a rodada possa ser concluída.

    Retorno:
        dict: {status: 0, mensagem: "N confronto(s) pendente(s) nesta rodada.",
               dados: [lista de tuplas (time1, time2) dos confrontos pendentes]}
              com dados não vazio se houver confrontos pendentes.
              {status: 0, mensagem: "Todos os confrontos da rodada foram registrados.",
               dados: []}
              se todos os confrontos já foram registrados.
              {status: 1, mensagem: "Nenhum torneio ativo...", dados: None}
              se não houver torneio ativo.

    Pré-condições:
        - nenhuma.

    Pós-condições:
        - O torneio ativo e _lista de partidas permanecem inalterados.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    t = _get_torneio(_torneio_ativo_id)
    if not t:
        return {"status": 1, "mensagem": "Nenhum torneio ativo para verificar confrontos pendentes.", "dados": None}
    registradas = partidas.por_rodada(t["rodada"], torneio_id=t["id"])["dados"]
    pendentes = []
    for c in t["confrontos"]:
        tem = any(
            (p["time1"] == c[0] and p["time2"] == c[1]) or
            (p["time1"] == c[1] and p["time2"] == c[0])
            for p in registradas
        )
        if not tem:
            pendentes.append(c)
    if pendentes:
        return {"status": 0, "mensagem": f"{len(pendentes)} confronto(s) pendente(s) nesta rodada.", "dados": pendentes}
    return {"status": 0, "mensagem": "Todos os confrontos da rodada foram registrados.", "dados": []}


def avancar() -> dict:
    """Avança para a próxima fase do torneio ou define o campeão.

    Em empate, ambos os times avançam. Quando restar um único time,
    ele é declarado campeão e os confrontos são esvaziados.

    Requisito:
        Conduzir a progressão do torneio de eliminação simples fase a fase.

    Retorno:
        dict: {status: 0, mensagem: "Avançado para a rodada N..." ou
               "Torneio encerrado. Campeão: ...", dados: None}
              em caso de sucesso.
              {status: 1, mensagem: "Nenhum torneio ativo encontrado.", dados: None}
              se não houver torneio ativo.
              {status: 1, mensagem: "Ainda há N confronto(s) pendente(s)...", dados: None}
              se ainda houver confrontos sem resultado na rodada atual.

    Pré-condições:
        - Deve existir um torneio ativo.
        - Todos os confrontos da rodada atual devem estar registrados.

    Pós-condições:
        - Em caso de sucesso (status 0) com 1 classificado: t["campeao"] é definido
          e t["confrontos"] = [].
        - Em caso de sucesso (status 0) com mais de 1 classificado: t["rodada"] é
          incrementado e novos confrontos são gerados.
        - Em caso de erro (status 1), o torneio permanece inalterado.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    t = _get_torneio(_torneio_ativo_id)
    if not t:
        return {"status": 1, "mensagem": "Nenhum torneio ativo encontrado.", "dados": None}
    pendentes = confrontos_pendentes()["dados"]
    if pendentes:
        return {"status": 1, "mensagem": f"Ainda há {len(pendentes)} confronto(s) pendente(s) nesta rodada.", "dados": None}
    resultados = partidas.por_rodada(t["rodada"], torneio_id=t["id"])["dados"]
    classificados = _avancar_fase(resultados)
    if len(classificados) == 1:
        t["campeao"] = classificados[0]
        t["confrontos"] = []
        return {"status": 0, "mensagem": f"Torneio encerrado. Campeão: {classificados[0]}.", "dados": None}
    t["rodada"] += 1
    t["confrontos"] = _gerar_confronto(classificados)
    return {"status": 0, "mensagem": f"Avançado para a rodada {t['rodada']} com {len(t['confrontos'])} confronto(s).", "dados": None}


def resetar_ativo() -> dict:
    """Reinicia o torneio ativo do zero mantendo os mesmos times.

    Requisito:
        Permitir recomeço do torneio ativo sem precisar recriá-lo.

    Retorno:
        dict: {status: 0, mensagem: "Torneio '...' reiniciado com sucesso.", dados: None}
              em caso de sucesso.
              {status: 1, mensagem: "Não há torneio ativo para reiniciar.", dados: None}
              se não houver torneio ativo.

    Pré-condições:
        - Deve existir um torneio ativo.

    Pós-condições:
        - Em caso de sucesso (status 0), t["rodada"] = 1, t["campeao"] = None
          e novos confrontos aleatórios são gerados com os times originais.
        - Em caso de erro (status 1), o estado permanece inalterado.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    t = _get_torneio(_torneio_ativo_id)
    if not t:
        return {"status": 1, "mensagem": "Não há torneio ativo para reiniciar.", "dados": None}
    t["rodada"] = 1
    t["campeao"] = None
    t["confrontos"] = _gerar_confronto(t["times"])
    return {"status": 0, "mensagem": f"Torneio '{t['nome']}' reiniciado com sucesso.", "dados": None}


def resetar() -> dict:
    """Remove todos os torneios e reinicia o estado completo do módulo.

    Requisito:
        Permitir limpeza total dos dados de torneios (uso administrativo).

    Retorno:
        dict: {status: 0, mensagem: "Todos os torneios removidos com sucesso.", dados: None}

    Pré-condições:
        - nenhuma.

    Pós-condições:
        - _torneios está vazio, _proximo_id = 1, _torneio_ativo_id = None.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    global _torneios, _proximo_id, _torneio_ativo_id
    _torneios.clear()
    _proximo_id = 1
    _torneio_ativo_id = None
    return {"status": 0, "mensagem": "Todos os torneios removidos com sucesso.", "dados": None}


def contexto_partida(time1: str, time2: str) -> dict:
    """Retorna o ID do torneio e a rodada se o par pertencer ao torneio ativo.

    Requisito:
        Associar automaticamente um resultado de partida ao torneio e rodada corretos.

    Parâmetros:
        time1 (str): Nome do primeiro time.
        time2 (str): Nome do segundo time.

    Retorno:
        dict: {status: 0, mensagem: "Confronto ativo encontrado.",
               dados: (torneio_id, rodada)}
              se o par for confronto ativo.
              {status: 1, mensagem: "Não é um confronto ativo ou não há torneio ativo.",
               dados: (None, None)}
              caso contrário.
              Dados é sempre uma tupla para permitir desempacotamento direto:
              torneio_id, rodada = resultado["dados"].

    Pré-condições:
        - time1 e time2 são strings.

    Pós-condições:
        - O torneio ativo permanece inalterado.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    t = _get_torneio(_torneio_ativo_id)
    if t and _eh_confronto_ativo(time1, time2):
        return {"status": 0, "mensagem": "Confronto ativo encontrado.", "dados": (t["id"], t["rodada"])}
    return {"status": 1, "mensagem": "Não é um confronto ativo ou não há torneio ativo.", "dados": (None, None)}


def salvar() -> dict:
    """Persiste o estado de todos os torneios no arquivo de dados.

    Requisito:
        Garantir durabilidade dos dados de torneios entre sessões.

    Retorno:
        dict: {status: 0, mensagem: "Torneios salvos com sucesso.", dados: None}
              Erros de I/O propagam exceção.

    Pré-condições:
        - _ARQUIVO aponta para um caminho gravável.

    Pós-condições:
        - O arquivo JSON reflete o estado atual de _torneios, _proximo_id
          e _torneio_ativo_id.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    _salvar()
    return {"status": 0, "mensagem": "Torneios salvos com sucesso.", "dados": None}
