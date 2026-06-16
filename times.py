import json
import os

__all__ = ["inicializar", "criar_time", "buscar_time", "listar_times", "remover_time", "parsear_jogadores", "salvar"]

_ARQUIVO = os.path.join(os.path.dirname(__file__), "dados", "times_data.json")
_ARQUIVO_INICIAL = os.path.join(os.path.dirname(__file__), "dados", "dados_iniciais.json")

_times = []
_proximo_id = 1


def _salvar() -> int:
    """Grava o estado atual dos times no arquivo JSON de persistência.

    Requisito:
        Persistir dados de times entre sessões da aplicação.

    Retorno:
        int: 0 sempre (escrita bem-sucedida; erros de I/O propagam exceção).

    Pré-condições:
        - _ARQUIVO aponta para um caminho gravável.

    Pós-condições:
        - O arquivo JSON em _ARQUIVO reflete o estado atual de _times e _proximo_id.

    Restrições:
        Interna — não exposta via __all__. Chamada exclusivamente por salvar().

    Interface:
        nenhuma
    """
    with open(_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump({"times": _times, "proximo_id": _proximo_id}, f, ensure_ascii=False, indent=2)
    return 0


def _carregar() -> int:
    """Lê os dados de times do arquivo JSON e popula as variáveis de módulo.

    Requisito:
        Restaurar estado de times ao iniciar a aplicação.

    Retorno:
        int: 0 se os dados foram carregados, 1 se nenhum arquivo foi encontrado.

    Pré-condições:
        - As variáveis globais _times e _proximo_id estão acessíveis.

    Pós-condições:
        - _times contém os times lidos do arquivo (ou [] se nenhum arquivo existir).
        - _proximo_id é maior que todos os IDs existentes.

    Restrições:
        Interna — não exposta via __all__. Chamada exclusivamente por inicializar().

    Interface:
        nenhuma
    """
    global _times, _proximo_id
    if os.path.exists(_ARQUIVO):
        with open(_ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)
        _times = dados.get("times", [])
        _proximo_id = dados.get("proximo_id", 1)
        return 0
    if os.path.exists(_ARQUIVO_INICIAL):
        with open(_ARQUIVO_INICIAL, "r", encoding="utf-8") as f:
            dados = json.load(f)
        _times = dados.get("times", [])
        if _times:
            _proximo_id = max(int(t["id"]) for t in _times) + 1
        return 0
    return 1


def inicializar() -> int:
    """Carrega os dados persistidos de times do arquivo para a memória.

    Requisito:
        Permitir que o módulo de times esteja pronto para uso ao iniciar a aplicação.

    Retorno:
        int: 0 se os dados foram carregados com sucesso, 1 se nenhum arquivo existir.

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


def criar_time(nome: str, jogadores: list) -> dict | str:
    """Cria e registra um novo time com ID único gerado automaticamente.

    Requisito:
        Permitir o cadastro de times com nome único e lista de jogadores.

    Parâmetros:
        nome (str): Nome do time. Não pode ser vazio nem duplicar um nome existente.
        jogadores (list): Lista de strings com os nomes dos jogadores. Pode ser [].

    Retorno:
        dict: {id, nome, jogadores} em caso de sucesso.
        str: Mensagem de erro se nome vazio ou duplicado.

    Pré-condições:
        - nome é uma string (pode estar em branco, erro será retornado).
        - jogadores é uma lista (None também é aceito e tratado como []).

    Pós-condições:
        - Em caso de sucesso, o time é adicionado a _times e _proximo_id é incrementado.
        - Em caso de erro, _times permanece inalterado.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    global _proximo_id
    if not nome or not nome.strip():
        return "Erro: nome do time não pode ser vazio."
    for time in _times:
        if time["nome"].lower() == nome.strip().lower():
            return f"Erro: já existe um time com o nome '{nome}'."
    novo_time = {
        "id": str(_proximo_id),
        "nome": nome.strip(),
        "jogadores": jogadores if jogadores is not None else [],
    }
    _proximo_id += 1
    _times.append(novo_time)
    return novo_time


def buscar_time(identificador: str) -> dict | str:
    """Localiza e retorna os dados de um time pelo seu ID.

    Requisito:
        Permitir consulta individual de time por identificador único.

    Parâmetros:
        identificador (str): ID do time a ser buscado.

    Retorno:
        dict: {id, nome, jogadores} se o time for encontrado.
        str: Mensagem de erro se ID vazio ou time não encontrado.

    Pré-condições:
        - identificador é uma string.

    Pós-condições:
        - _times permanece inalterado.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    if not identificador or not identificador.strip():
        return "Erro: ID não pode ser vazio."
    for time in _times:
        if time["id"] == identificador:
            return time
    return f"Erro: time com ID '{identificador}' não encontrado."


def listar_times() -> list:
    """Retorna cópia da lista de todos os times cadastrados.

    Requisito:
        Permitir visualização de todos os times disponíveis.

    Retorno:
        list: Lista de dicts {id, nome, jogadores}; [] se não houver times.

    Pré-condições:
        - nenhuma.

    Pós-condições:
        - _times permanece inalterado (retorna cópia rasa).

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    return list(_times)


def remover_time(identificador: str) -> str:
    """Remove um time da lista interna pelo seu ID.

    Requisito:
        Permitir exclusão de times cadastrados.

    Parâmetros:
        identificador (str): ID do time a ser removido.

    Retorno:
        str: Mensagem de sucesso com o nome do time removido.
             Mensagem de erro se ID vazio ou time não encontrado.

    Pré-condições:
        - identificador é uma string.

    Pós-condições:
        - Em caso de sucesso, o time é retirado de _times.
        - Em caso de erro, _times permanece inalterado.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    if not identificador or not identificador.strip():
        return "Erro: ID não pode ser vazio."
    for i, time in enumerate(_times):
        if time["id"] == identificador:
            nome = time["nome"]
            _times.pop(i)
            return f"Time '{nome}' removido com sucesso."
    return f"Erro: time com ID '{identificador}' não encontrado."


def parsear_jogadores(raw: str) -> list:
    """Converte uma string de nomes separados por vírgula em lista de strings.

    Requisito:
        Permitir entrada de múltiplos jogadores em um único campo de texto.

    Parâmetros:
        raw (str): String com nomes separados por vírgula. Pode ser vazia ou None.

    Retorno:
        list: Lista de strings com nomes sem espaços extras; [] se raw for vazio/None.

    Pré-condições:
        - raw é uma string ou None.

    Pós-condições:
        - Cada elemento da lista retornada é uma string não vazia sem espaços extras.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    return [j.strip() for j in raw.split(",") if j.strip()] if raw else []


def salvar() -> int:
    """Persiste o estado atual dos times no arquivo de dados.

    Requisito:
        Garantir durabilidade dos dados de times entre sessões.

    Retorno:
        int: 0 em caso de sucesso; erros de I/O propagam exceção.

    Pré-condições:
        - _ARQUIVO aponta para um caminho gravável.

    Pós-condições:
        - O arquivo JSON reflete o estado atual de _times e _proximo_id.

    Restrições:
        Pública — exposta via __all__.

    Interface:
        nenhuma
    """
    return _salvar()
