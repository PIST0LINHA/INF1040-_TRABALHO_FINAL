import json
import os

__all__ = ["criar_time", "buscar_time", "listar_times", "remover_time", "salvar"]

_ARQUIVO = os.path.join(os.path.dirname(__file__), "..", "dados", "times_data.json")
_ARQUIVO_INICIAL = os.path.join(os.path.dirname(__file__), "..", "dados", "dados_iniciais.json")

_times = []
_proximo_id = 1


def _salvar() -> int:
    with open(_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump({"times": _times, "proximo_id": _proximo_id}, f, ensure_ascii=False, indent=2)
    return 0


def _carregar() -> int:
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


_carregar()


def criar_time(nome: str, jogadores: list) -> dict:
    """Cria um novo time com ID único gerado automaticamente.

    Parâmetros:
        nome: nome do time (não pode ser vazio nem duplicado)
        jogadores: lista de nomes dos jogadores

    Retorno:
        dict com id, nome e jogadores em caso de sucesso
        str com mensagem de erro em caso de falha
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


def buscar_time(identificador: str) -> dict:
    """Busca um time pelo ID.

    Parâmetros:
        identificador: ID do time

    Retorno:
        dict com os dados do time se encontrado
        str com mensagem de erro se ID inválido ou não encontrado
    """
    if not identificador or not identificador.strip():
        return "Erro: ID não pode ser vazio."
    for time in _times:
        if time["id"] == identificador:
            return time
    return f"Erro: time com ID '{identificador}' não encontrado."


def listar_times() -> list:
    """Retorna a lista de todos os times cadastrados.

    Retorno:
        list de dicts, cada um com id, nome e jogadores
    """
    return list(_times)


def remover_time(identificador: str) -> str:
    """Remove um time pelo ID.

    Parâmetros:
        identificador: ID do time a remover

    Retorno:
        str com mensagem de sucesso ou de erro
    """
    if not identificador or not identificador.strip():
        return "Erro: ID não pode ser vazio."
    for i, time in enumerate(_times):
        if time["id"] == identificador:
            nome = time["nome"]
            _times.pop(i)
            return f"Time '{nome}' removido com sucesso."
    return f"Erro: time com ID '{identificador}' não encontrado."


def salvar() -> int:
    """Persiste o estado atual dos times no arquivo de dados.

    Retorno:
        0 em caso de sucesso
    """
    return _salvar()
