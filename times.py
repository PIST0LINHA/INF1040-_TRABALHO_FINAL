_times = []
_proximo_id = 1


def criar_time(nome, jogadores):
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
