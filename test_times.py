import times

resultados = []


def registrar(nome_teste, passou, detalhe=""):
    resultados.append({"teste": nome_teste, "passou": passou, "detalhe": detalhe})


def limpar_times():
    ids = [t["id"] for t in times.listar_times()]
    for id_ in ids:
        times.remover_time(id_)


# --- criar_time ---

def teste_criar_time_valido():
    limpar_times()
    resultado = times.criar_time("Flamengo", ["Jogador1", "Jogador2"])
    passou = (
        isinstance(resultado, dict)
        and "id" in resultado
        and resultado["nome"] == "Flamengo"
        and resultado["jogadores"] == ["Jogador1", "Jogador2"]
    )
    registrar("criar_time: nome e jogadores válidos", passou, str(resultado))


def teste_criar_time_jogadores_vazios():
    limpar_times()
    resultado = times.criar_time("Vasco", [])
    passou = isinstance(resultado, dict) and resultado["jogadores"] == []
    registrar("criar_time: lista de jogadores vazia", passou, str(resultado))


# --- buscar_time ---

def teste_buscar_time_existente():
    limpar_times()
    criado = times.criar_time("Botafogo", ["Ana"])
    resultado = times.buscar_time(criado["id"])
    passou = isinstance(resultado, dict) and resultado["id"] == criado["id"]
    registrar("buscar_time: ID existente", passou, str(resultado))


def teste_buscar_time_inexistente():
    resultado = times.buscar_time("zzzzzz")
    passou = isinstance(resultado, str) and "não encontrado" in resultado and "zzzzzz" in resultado
    registrar("buscar_time: ID inexistente", passou, str(resultado))


def teste_buscar_time_id_vazio():
    resultado = times.buscar_time("")
    passou = resultado == "Erro: ID não pode ser vazio."
    registrar("buscar_time: ID vazio", passou, str(resultado))


# --- listar_times ---

def teste_listar_times_com_times():
    limpar_times()
    times.criar_time("Palmeiras", [])
    times.criar_time("Santos", [])
    resultado = times.listar_times()
    passou = isinstance(resultado, list) and len(resultado) == 2
    registrar("listar_times: com times cadastrados", passou, str(resultado))


def teste_listar_times_vazio():
    limpar_times()
    resultado = times.listar_times()
    passou = resultado == []
    registrar("listar_times: sem times cadastrados", passou, str(resultado))


# --- remover_time ---

def teste_remover_time_existente():
    limpar_times()
    criado = times.criar_time("Corinthians", [])
    resultado = times.remover_time(criado["id"])
    ainda_existe = any(t["id"] == criado["id"] for t in times.listar_times())
    passou = (
        isinstance(resultado, str)
        and "removido com sucesso" in resultado
        and not ainda_existe
    )
    registrar("remover_time: ID existente", passou, str(resultado))


def teste_remover_time_inexistente():
    resultado = times.remover_time("zzzzzz")
    passou = isinstance(resultado, str) and "não encontrado" in resultado and "zzzzzz" in resultado
    registrar("remover_time: ID inexistente", passou, str(resultado))


def teste_remover_time_id_vazio():
    resultado = times.remover_time("")
    passou = resultado == "Erro: ID não pode ser vazio."
    registrar("remover_time: ID vazio", passou, str(resultado))


# --- execução ---

def executar_testes():
    testes = [
        teste_criar_time_valido,
        teste_criar_time_jogadores_vazios,
        teste_buscar_time_existente,
        teste_buscar_time_inexistente,
        teste_buscar_time_id_vazio,
        teste_listar_times_com_times,
        teste_listar_times_vazio,
        teste_remover_time_existente,
        teste_remover_time_inexistente,
        teste_remover_time_id_vazio,
    ]

    for teste in testes:
        try:
            teste()
        except Exception as e:
            nome = teste.__name__.replace("teste_", "").replace("_", " ")
            registrar(nome, False, f"Exceção: {e}")

    print("\nRelatório de Testes — times.py\n")
    passaram = 0
    falharam = 0
    for r in resultados:
        status = "PASSOU" if r["passou"] else "FALHOU"
        print(f"  [{status}] {r['teste']}")
        if not r["passou"]:
            print(f"          Detalhe: {r['detalhe']}")
            falharam += 1
        else:
            passaram += 1

    print(f"\nTotal: {passaram} passaram, {falharam} falharam\n")


executar_testes()
