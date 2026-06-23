import sys, os, tempfile; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import times

# Isolamento: testes nunca escrevem nos arquivos reais de dados/.
times._ARQUIVO = os.path.join(tempfile.gettempdir(), "test_times_data.json")

resultados = []


def registrar(nome_teste, passou, detalhe=""):
    resultados.append({"teste": nome_teste, "passou": passou, "detalhe": detalhe})


def limpar_times():
    for t in times.listar_times()["dados"]:
        times.remover_time(t["id"])


# --- criar_time ---

def teste_criar_time_valido():
    limpar_times()
    r = times.criar_time("Flamengo", ["Jogador1", "Jogador2"])
    passou = (
        r["status"] == 0
        and r["dados"]["nome"] == "Flamengo"
        and r["dados"]["jogadores"] == ["Jogador1", "Jogador2"]
        and "id" in r["dados"]
    )
    registrar("criar_time: nome e jogadores válidos retorna status 0 e dados corretos", passou, str(r))


def teste_criar_time_jogadores_vazios():
    limpar_times()
    r = times.criar_time("Vasco", [])
    passou = r["status"] == 0 and r["dados"]["jogadores"] == []
    registrar("criar_time: lista de jogadores vazia retorna status 0", passou, str(r))


def teste_criar_time_nome_vazio():
    r = times.criar_time("", [])
    passou = r["status"] == 1 and "Erro" in r["mensagem"]
    registrar("criar_time: nome vazio retorna status 1 com mensagem de erro", passou, str(r))


def teste_criar_time_nome_duplicado():
    limpar_times()
    times.criar_time("Botafogo", [])
    r = times.criar_time("Botafogo", [])
    passou = r["status"] == 1 and "Botafogo" in r["mensagem"]
    registrar("criar_time: nome duplicado retorna status 1 com mensagem de erro", passou, str(r))


# --- buscar_time ---

def teste_buscar_time_existente():
    limpar_times()
    criado = times.criar_time("Botafogo", ["Ana"])
    r = times.buscar_time(criado["dados"]["id"])
    passou = r["status"] == 0 and r["dados"]["id"] == criado["dados"]["id"]
    registrar("buscar_time: ID existente retorna status 0 e dados do time", passou, str(r))


def teste_buscar_time_inexistente():
    r = times.buscar_time("zzzzzz")
    passou = r["status"] == 1 and "não encontrado" in r["mensagem"] and "zzzzzz" in r["mensagem"]
    registrar("buscar_time: ID inexistente retorna status 1 com mensagem de erro", passou, str(r))


def teste_buscar_time_id_vazio():
    r = times.buscar_time("")
    passou = r["status"] == 1 and "ID não pode ser vazio" in r["mensagem"]
    registrar("buscar_time: ID vazio retorna status 1 com mensagem de erro", passou, str(r))


# --- listar_times ---

def teste_listar_times_com_times():
    limpar_times()
    times.criar_time("Palmeiras", [])
    times.criar_time("Santos", [])
    r = times.listar_times()
    passou = r["status"] == 0 and isinstance(r["dados"], list) and len(r["dados"]) == 2
    registrar("listar_times: com times cadastrados retorna status 0 e lista com 2 times", passou, str(r))


def teste_listar_times_vazio():
    limpar_times()
    r = times.listar_times()
    passou = r["status"] == 0 and r["dados"] == []
    registrar("listar_times: sem times cadastrados retorna status 0 e lista vazia", passou, str(r))


# --- remover_time ---

def teste_remover_time_existente():
    limpar_times()
    criado = times.criar_time("Corinthians", [])
    r = times.remover_time(criado["dados"]["id"])
    ainda_existe = any(t["id"] == criado["dados"]["id"] for t in times.listar_times()["dados"])
    passou = r["status"] == 0 and r["dados"]["nome"] == "Corinthians" and not ainda_existe
    registrar("remover_time: ID existente retorna status 0 e dados do time removido", passou, str(r))


def teste_remover_time_inexistente():
    r = times.remover_time("zzzzzz")
    passou = r["status"] == 1 and "não encontrado" in r["mensagem"] and "zzzzzz" in r["mensagem"]
    registrar("remover_time: ID inexistente retorna status 1 com mensagem de erro", passou, str(r))


def teste_remover_time_id_vazio():
    r = times.remover_time("")
    passou = r["status"] == 1 and "ID não pode ser vazio" in r["mensagem"]
    registrar("remover_time: ID vazio retorna status 1 com mensagem de erro", passou, str(r))


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

def teste_salvar_retorna_status_zero():
    limpar_times()
    times.criar_time("Flamengo", [])
    r = times.salvar()
    passou = r["status"] == 0
    registrar("salvar: persiste dados e retorna status 0", passou, str(r))


def teste_inicializar_retorna_dict():
    r = times.inicializar()
    passou = isinstance(r, dict) and "status" in r and "mensagem" in r and "dados" in r
    registrar("inicializar: retorna dict com status, mensagem e dados", passou, str(r))


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
        teste_salvar_retorna_status_zero,
        teste_inicializar_retorna_dict,
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
