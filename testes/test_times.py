import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import times

resultados = []


def registrar(nome_teste, passou, detalhe=""):
    resultados.append({"teste": nome_teste, "passou": passou, "detalhe": detalhe})


def limpar_times():
    for t in times.listar_times():
        times.remover_time(t["id"])


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


def teste_criar_time_nome_vazio():
    resultado = times.criar_time("", [])
    passou = isinstance(resultado, str) and resultado.startswith("Erro")
    registrar("criar_time: nome vazio retorna mensagem de erro", passou, str(resultado))


def teste_criar_time_nome_duplicado():
    limpar_times()
    times.criar_time("Botafogo", [])
    resultado = times.criar_time("Botafogo", [])
    passou = isinstance(resultado, str) and "Botafogo" in resultado
    registrar("criar_time: nome duplicado retorna mensagem de erro", passou, str(resultado))


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


# --- parsear_jogadores ---

def teste_parsear_jogadores_string_valida():
    resultado = times.parsear_jogadores("Ana, Bruno, Carlos")
    passou = resultado == ["Ana", "Bruno", "Carlos"]
    registrar("parsear_jogadores: string com nomes separados por vírgula", passou, str(resultado))


def teste_parsear_jogadores_string_vazia():
    resultado = times.parsear_jogadores("")
    passou = resultado == []
    registrar("parsear_jogadores: string vazia retorna lista vazia", passou, str(resultado))


def teste_parsear_jogadores_espacos_extras():
    resultado = times.parsear_jogadores("  Ana ,  Bruno  ")
    passou = resultado == ["Ana", "Bruno"]
    registrar("parsear_jogadores: espaços extras são removidos", passou, str(resultado))


# --- inicializar / salvar ---

def teste_salvar_retorna_zero():
    limpar_times()
    times.criar_time("Flamengo", [])
    resultado = times.salvar()
    passou = resultado == 0
    registrar("salvar: persiste dados e retorna 0", passou, str(resultado))


def teste_inicializar_retorna_inteiro():
    resultado = times.inicializar()
    passou = isinstance(resultado, int)
    registrar("inicializar: retorna int (0 se arquivo existe, 1 se não existe)", passou, str(resultado))


# --- execução ---

def executar_testes():
    testes = [
        teste_criar_time_valido,
        teste_criar_time_jogadores_vazios,
        teste_criar_time_nome_vazio,
        teste_criar_time_nome_duplicado,
        teste_buscar_time_existente,
        teste_buscar_time_inexistente,
        teste_buscar_time_id_vazio,
        teste_listar_times_com_times,
        teste_listar_times_vazio,
        teste_remover_time_existente,
        teste_remover_time_inexistente,
        teste_remover_time_id_vazio,
        teste_parsear_jogadores_string_valida,
        teste_parsear_jogadores_string_vazia,
        teste_parsear_jogadores_espacos_extras,
        teste_salvar_retorna_zero,
        teste_inicializar_retorna_inteiro,
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
