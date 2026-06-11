import json
import os

_times = []
_proximo_id = 1


def _carregar_dados_iniciais():
    global _times, _proximo_id
    caminho = os.path.join(os.path.dirname(__file__), "dados_iniciais.json")
    if not os.path.exists(caminho):
        return
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
    _times = dados.get("times", [])
    if _times:
        _proximo_id = max(int(t["id"]) for t in _times) + 1


_carregar_dados_iniciais()


def criar_time(nome, jogadores):
    global _proximo_id

    if not nome or not nome.strip():
        return "Erro: nome do time não pode ser vazio."

    for time in _times:
        if time["nome"].lower() == nome.strip().lower():
            return f"Erro: já existe um time com o nome '{nome}'."

    id_time = str(_proximo_id)

    novo_time = {
        "id": id_time,
        "nome": nome.strip(),
        "jogadores": jogadores if jogadores is not None else [],
    }
    _proximo_id += 1
    _times.append(novo_time)
    return novo_time


def buscar_time(identificador):
    if not identificador or not identificador.strip():
        return "Erro: ID não pode ser vazio."

    for time in _times:
        if time["id"] == identificador:
            return time

    return f"Erro: time com ID '{identificador}' não encontrado."


def listar_times():
    return list(_times)


def remover_time(identificador):
    if not identificador or not identificador.strip():
        return "Erro: ID não pode ser vazio."

    for i, time in enumerate(_times):
        if time["id"] == identificador:
            nome = time["nome"]
            _times.pop(i)
            return f"Time '{nome}' removido com sucesso."

    return f"Erro: time com ID '{identificador}' não encontrado."
