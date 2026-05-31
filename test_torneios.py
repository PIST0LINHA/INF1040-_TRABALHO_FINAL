import torneios

resultados = []


def registrar(nome_teste, passou, detalhe=""):
    resultados.append({"teste": nome_teste, "passou": passou, "detalhe": detalhe})


# --- gerar_confronto ---

def teste_gerar_confronto_par_de_times():
    lista = ["Flamengo", "Vasco", "Fluminense", "Botafogo"]
    confrontos = torneios.gerar_confronto(lista)
    passou = (
        isinstance(confrontos, list)
        and len(confrontos) == 2
        and all(isinstance(c, tuple) and len(c) == 2 for c in confrontos)
    )
    if passou:
        envolvidos = [t for c in confrontos for t in c]
        passou = sorted(envolvidos) == sorted(lista)
    registrar("gerar_confronto: lista com número par de times", passou, str(confrontos))


def teste_gerar_confronto_dois_times():
    lista = ["Flamengo", "Vasco"]
    confrontos = torneios.gerar_confronto(lista)
    passou = (
        isinstance(confrontos, list)
        and len(confrontos) == 1
        and isinstance(confrontos[0], tuple)
        and len(confrontos[0]) == 2
        and sorted(confrontos[0]) == sorted(lista)
    )
    registrar("gerar_confronto: lista com 2 times", passou, str(confrontos))


def teste_gerar_confronto_lista_vazia():
    confrontos = torneios.gerar_confronto([])
    passou = confrontos == []
    registrar("gerar_confronto: lista vazia", passou, str(confrontos))


# --- iniciar_rodada ---

def teste_iniciar_rodada_multiplos_confrontos():
    confrontos = [("Flamengo", "Vasco"), ("Fluminense", "Botafogo")]
    rodada = torneios.iniciar_rodada(confrontos)
    passou = isinstance(rodada, list) and len(rodada) == 2
    if passou:
        for i, partida in enumerate(rodada):
            esperado_t1, esperado_t2 = confrontos[i]
            ok = (
                isinstance(partida, dict)
                and partida.get("time1") == esperado_t1
                and partida.get("time2") == esperado_t2
                and isinstance(partida.get("gols_time1"), int)
                and isinstance(partida.get("gols_time2"), int)
                and partida["gols_time1"] >= 0
                and partida["gols_time2"] >= 0
            )
            if not ok:
                passou = False
                break
    registrar("iniciar_rodada: múltiplos confrontos", passou, str(rodada))


def teste_iniciar_rodada_confronto_unico():
    confrontos = [("Flamengo", "Vasco")]
    rodada = torneios.iniciar_rodada(confrontos)
    passou = (
        isinstance(rodada, list)
        and len(rodada) == 1
        and isinstance(rodada[0], dict)
        and rodada[0].get("time1") == "Flamengo"
        and rodada[0].get("time2") == "Vasco"
        and isinstance(rodada[0].get("gols_time1"), int)
        and isinstance(rodada[0].get("gols_time2"), int)
    )
    registrar("iniciar_rodada: confronto único", passou, str(rodada))


def teste_iniciar_rodada_lista_vazia():
    rodada = torneios.iniciar_rodada([])
    passou = rodada == []
    registrar("iniciar_rodada: lista vazia", passou, str(rodada))


# --- avancar_fase ---

def teste_avancar_fase_vencedor_claro():
    resultados = [{"time1": "Flamengo", "time2": "Vasco", "gols_time1": 2, "gols_time2": 0}]
    classificados = torneios.avancar_fase(resultados)
    passou = classificados == ["Flamengo"]
    registrar("avancar_fase: vencedor claro avança", passou, str(classificados))


def teste_avancar_fase_empate():
    resultados = [{"time1": "Flamengo", "time2": "Vasco", "gols_time1": 1, "gols_time2": 1}]
    classificados = torneios.avancar_fase(resultados)
    passou = (
        isinstance(classificados, list)
        and sorted(classificados) == ["Flamengo", "Vasco"]
    )
    registrar("avancar_fase: empate, ambos avançam", passou, str(classificados))


def teste_avancar_fase_multiplas_partidas():
    resultados = [
        {"time1": "Flamengo", "time2": "Vasco", "gols_time1": 3, "gols_time2": 1},
        {"time1": "Fluminense", "time2": "Botafogo", "gols_time1": 0, "gols_time2": 2},
    ]
    classificados = torneios.avancar_fase(resultados)
    passou = classificados == ["Flamengo", "Botafogo"]
    registrar("avancar_fase: múltiplas partidas, cada vencedor avança", passou, str(classificados))


def executar_testes():
    testes = [
        teste_gerar_confronto_par_de_times,
        teste_gerar_confronto_dois_times,
        teste_gerar_confronto_lista_vazia,
        teste_iniciar_rodada_multiplos_confrontos,
        teste_iniciar_rodada_confronto_unico,
        teste_iniciar_rodada_lista_vazia,
        teste_avancar_fase_vencedor_claro,
        teste_avancar_fase_empate,
        teste_avancar_fase_multiplas_partidas,
    ]

    for teste in testes:
        try:
            teste()
        except Exception as e:
            nome = teste.__name__.replace("teste_", "").replace("_", " ")
            registrar(nome, False, f"Exceção: {e}")

    print("\nRelatório de Testes — torneios.py\n")
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
