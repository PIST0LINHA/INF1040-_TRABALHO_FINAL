import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import ranking

resultados = []


def registrar(nome_teste, passou, detalhe=""):
    resultados.append({"teste": nome_teste, "passou": passou, "detalhe": detalhe})


def resetar():
    ranking.criar_tabela(["Flamengo", "Vasco", "Fluminense", "Botafogo"])


# --- criar_tabela ---

def teste_criar_tabela_multiplos_times():
    ranking.criar_tabela(["Flamengo", "Vasco", "Fluminense"])
    relacao = ranking.ordenar_classificacao()["dados"]
    passou = (
        len(relacao) == 3
        and all(t["pontos"] == 0 for t in relacao)
        and all(t["vitorias"] == 0 for t in relacao)
        and all(t["empates"] == 0 for t in relacao)
        and all(t["derrotas"] == 0 for t in relacao)
        and all(t["gols_marcados"] == 0 for t in relacao)
        and all(t["gols_sofridos"] == 0 for t in relacao)
    )
    registrar("criar_tabela: múltiplos times com contadores zerados", passou, str(relacao))


def teste_criar_tabela_nome_preservado():
    ranking.criar_tabela(["Flamengo"])
    relacao = ranking.ordenar_classificacao()["dados"]
    passou = relacao[0]["time"] == "Flamengo"
    registrar("criar_tabela: nome do time preservado", passou, str(relacao))


def teste_criar_tabela_lista_vazia():
    ranking.criar_tabela([])
    relacao = ranking.ordenar_classificacao()["dados"]
    passou = relacao == []
    registrar("criar_tabela: lista vazia não gera erro", passou, str(relacao))


def teste_criar_tabela_torneio_id_vazio_retorna_status_um():
    r = ranking.criar_tabela(["Flamengo"], torneio_id="")
    passou = r["status"] == 1
    registrar("criar_tabela: torneio_id vazio retorna status 1", passou, str(r))


def teste_criar_tabela_retorna_status_zero():
    r = ranking.criar_tabela(["Flamengo", "Vasco"])
    passou = r["status"] == 0
    registrar("criar_tabela: entrada válida retorna status 0", passou, str(r))


# --- atualizar_pontos ---

def teste_atualizar_pontos_vitoria_time1():
    ranking.criar_tabela(["Flamengo", "Vasco"])
    ranking.atualizar_pontos({"time1": "Flamengo", "gols_time1": 2,
                               "time2": "Vasco",    "gols_time2": 0})
    relacao  = ranking.ordenar_classificacao()["dados"]
    flamengo = next(t for t in relacao if t["time"] == "Flamengo")
    vasco    = next(t for t in relacao if t["time"] == "Vasco")
    passou = (
        flamengo["pontos"] == 3 and flamengo["vitorias"] == 1 and flamengo["derrotas"] == 0
        and vasco["pontos"] == 0 and vasco["vitorias"] == 0 and vasco["derrotas"] == 1
    )
    registrar("atualizar_pontos: vitória do time da casa", passou,
              f"Flamengo={flamengo} | Vasco={vasco}")


def teste_atualizar_pontos_vitoria_time_fora():
    ranking.criar_tabela(["Flamengo", "Vasco"])
    ranking.atualizar_pontos({"time1": "Flamengo", "gols_time1": 0,
                               "time2": "Vasco",    "gols_time2": 7})
    relacao  = ranking.ordenar_classificacao()["dados"]
    flamengo = next(t for t in relacao if t["time"] == "Flamengo")
    vasco    = next(t for t in relacao if t["time"] == "Vasco")
    passou = (
        vasco["pontos"] == 3 and vasco["vitorias"] == 1 and vasco["derrotas"] == 0
        and flamengo["pontos"] == 0 and flamengo["vitorias"] == 0 and flamengo["derrotas"] == 1
    )
    registrar("atualizar_pontos: vitória do time de fora", passou,
              f"Flamengo={flamengo} | Vasco={vasco}")


def teste_atualizar_pontos_empate():
    ranking.criar_tabela(["Flamengo", "Vasco"])
    ranking.atualizar_pontos({"time1": "Flamengo", "gols_time1": 1,
                               "time2": "Vasco",    "gols_time2": 1})
    relacao  = ranking.ordenar_classificacao()["dados"]
    flamengo = next(t for t in relacao if t["time"] == "Flamengo")
    vasco    = next(t for t in relacao if t["time"] == "Vasco")
    passou = (
        flamengo["pontos"] == 1 and flamengo["empates"] == 1
        and vasco["pontos"] == 1 and vasco["empates"] == 1
    )
    registrar("atualizar_pontos: empate", passou,
              f"Flamengo={flamengo} | Vasco={vasco}")


def teste_atualizar_pontos_gols_contabilizados():
    ranking.criar_tabela(["Flamengo", "Vasco"])
    ranking.atualizar_pontos({"time1": "Flamengo", "gols_time1": 3,
                               "time2": "Vasco",    "gols_time2": 1})
    relacao  = ranking.ordenar_classificacao()["dados"]
    flamengo = next(t for t in relacao if t["time"] == "Flamengo")
    vasco    = next(t for t in relacao if t["time"] == "Vasco")
    passou = (
        flamengo["gols_marcados"] == 3 and flamengo["gols_sofridos"] == 1
        and vasco["gols_marcados"] == 1 and vasco["gols_sofridos"] == 3
    )
    registrar("atualizar_pontos: gols contabilizados corretamente", passou,
              f"Flamengo={flamengo} | Vasco={vasco}")


def teste_atualizar_pontos_acumulativo():
    ranking.criar_tabela(["Flamengo", "Vasco"])
    ranking.atualizar_pontos({"time1": "Flamengo", "gols_time1": 2,
                               "time2": "Vasco",    "gols_time2": 0})
    ranking.atualizar_pontos({"time1": "Flamengo", "gols_time1": 1,
                               "time2": "Vasco",    "gols_time2": 1})
    relacao  = ranking.ordenar_classificacao()["dados"]
    flamengo = next(t for t in relacao if t["time"] == "Flamengo")
    passou = (
        flamengo["pontos"] == 4
        and flamengo["vitorias"] == 1
        and flamengo["empates"] == 1
        and flamengo["gols_marcados"] == 3
        and flamengo["gols_sofridos"] == 1
    )
    registrar("atualizar_pontos: acumulativo após 2 partidas", passou, str(flamengo))


# --- ordenar_classificacao ---

def teste_ordenar_classificacao_por_pontos():
    ranking.criar_tabela(["Flamengo", "Vasco", "Fluminense"])
    ranking.atualizar_pontos({"time1": "Fluminense", "gols_time1": 1, "time2": "Flamengo",   "gols_time2": 0})
    ranking.atualizar_pontos({"time1": "Fluminense", "gols_time1": 1, "time2": "Vasco",      "gols_time2": 0})
    ranking.atualizar_pontos({"time1": "Fluminense", "gols_time1": 1, "time2": "Vasco",      "gols_time2": 0})
    ranking.atualizar_pontos({"time1": "Flamengo",   "gols_time1": 1, "time2": "Vasco",      "gols_time2": 0})
    ranking.atualizar_pontos({"time1": "Flamengo",   "gols_time1": 1, "time2": "Vasco",      "gols_time2": 0})
    ranking.atualizar_pontos({"time1": "Vasco",      "gols_time1": 1, "time2": "Flamengo",   "gols_time2": 0})
    relacao = ranking.ordenar_classificacao()["dados"]
    passou = (
        relacao[0]["time"] == "Fluminense"
        and relacao[1]["time"] == "Flamengo"
        and relacao[2]["time"] == "Vasco"
    )
    registrar("ordenar_classificacao: ordenação por pontos", passou, str(relacao))


def teste_ordenar_classificacao_desempate_vitorias():
    ranking.criar_tabela(["Flamengo", "Vasco"])
    ranking.atualizar_pontos({"time1": "Flamengo", "gols_time1": 1,
                               "time2": "Vasco",    "gols_time2": 0})
    relacao = ranking.ordenar_classificacao()["dados"]
    passou = (
        relacao[0]["time"] == "Flamengo" and relacao[0]["vitorias"] == 1
        and relacao[1]["time"] == "Vasco" and relacao[1]["vitorias"] == 0
    )
    registrar("ordenar_classificacao: desempate por vitórias", passou, str(relacao))


def teste_ordenar_classificacao_desempate_saldo_gols():
    ranking.criar_tabela(["Flamengo", "Vasco", "Fluminense"])
    ranking.atualizar_pontos({"time1": "Flamengo",   "gols_time1": 3,
                               "time2": "Fluminense", "gols_time2": 1})
    ranking.atualizar_pontos({"time1": "Vasco",      "gols_time1": 2,
                               "time2": "Fluminense", "gols_time2": 1})
    relacao  = ranking.ordenar_classificacao()["dados"]
    flamengo = next(t for t in relacao if t["time"] == "Flamengo")
    vasco    = next(t for t in relacao if t["time"] == "Vasco")
    passou = relacao.index(flamengo) < relacao.index(vasco)
    registrar("ordenar_classificacao: desempate por saldo de gols", passou, str(relacao))


def teste_ordenar_classificacao_tabela_original_nao_modificada():
    ranking.criar_tabela(["Flamengo", "Vasco"])
    ranking.atualizar_pontos({"time1": "Vasco",    "gols_time1": 3,
                               "time2": "Flamengo", "gols_time2": 0})
    primeiro_antes = ranking.ordenar_classificacao()["dados"][0]["time"]
    ranking.ordenar_classificacao()
    primeiro_depois = ranking.ordenar_classificacao()["dados"][0]["time"]
    passou = primeiro_depois == primeiro_antes
    registrar("ordenar_classificacao: tabela original não modificada", passou,
              f"antes={primeiro_antes} | depois={primeiro_depois}")


def teste_ordenar_classificacao_torneio_inexistente_retorna_status_um():
    r = ranking.ordenar_classificacao("torneio_que_nao_existe_xyz")
    passou = r["status"] == 1 and r["dados"] is None
    registrar("ordenar_classificacao: torneio inexistente retorna status 1 e dados None", passou, str(r))


# --- inicializar / salvar ---

def teste_inicializar_retorna_dict():
    r = ranking.inicializar()
    passou = isinstance(r, dict) and "status" in r and "mensagem" in r and "dados" in r
    registrar("inicializar: retorna dict com status, mensagem e dados", passou, str(r))


def teste_salvar_retorna_status_zero():
    ranking.criar_tabela(["Flamengo", "Vasco"])
    r = ranking.salvar()
    passou = r["status"] == 0
    registrar("salvar: persiste dados e retorna status 0", passou, str(r))


# --- atualizar_pontos (cenários de falha) ---

def teste_atualizar_pontos_torneio_inexistente():
    r = ranking.atualizar_pontos(
        {"time1": "Flamengo", "gols_time1": 1, "time2": "Vasco", "gols_time2": 0},
        torneio_id="torneio_que_nao_existe"
    )
    passou = r["status"] == 1
    registrar("atualizar_pontos: torneio inexistente retorna status 1", passou, str(r))


def teste_atualizar_pontos_time_nao_encontrado():
    ranking.criar_tabela(["Flamengo", "Vasco"])
    r = ranking.atualizar_pontos(
        {"time1": "Palmeiras", "gols_time1": 1, "time2": "Santos", "gols_time2": 0}
    )
    passou = r["status"] == 1
    registrar("atualizar_pontos: times não encontrados na tabela retorna status 1", passou, str(r))


# --- execução ---

def executar_testes():
    testes = [
        teste_criar_tabela_multiplos_times,
        teste_criar_tabela_nome_preservado,
        teste_criar_tabela_lista_vazia,
        teste_criar_tabela_torneio_id_vazio_retorna_status_um,
        teste_criar_tabela_retorna_status_zero,
        teste_atualizar_pontos_vitoria_time1,
        teste_atualizar_pontos_vitoria_time_fora,
        teste_atualizar_pontos_empate,
        teste_atualizar_pontos_gols_contabilizados,
        teste_atualizar_pontos_acumulativo,
        teste_ordenar_classificacao_por_pontos,
        teste_ordenar_classificacao_desempate_vitorias,
        teste_ordenar_classificacao_desempate_saldo_gols,
        teste_ordenar_classificacao_tabela_original_nao_modificada,
        teste_ordenar_classificacao_torneio_inexistente_retorna_status_um,
        teste_inicializar_retorna_dict,
        teste_salvar_retorna_status_zero,
        teste_atualizar_pontos_torneio_inexistente,
        teste_atualizar_pontos_time_nao_encontrado,
    ]

    for teste in testes:
        try:
            teste()
        except Exception as e:
            nome = teste.__name__.replace("teste_", "").replace("_", " ")
            registrar(nome, False, f"Exceção: {e}")

    print("\nRelatório de Testes — ranking.py\n")
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
