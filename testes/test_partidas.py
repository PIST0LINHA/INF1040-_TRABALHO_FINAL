import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import partidas

resultados = []


def registrar(nome_teste, passou, detalhe=""):
    resultados.append({"teste": nome_teste, "passou": passou, "detalhe": detalhe})


def resetar_estado():
    partidas.resetar()


# --- registrar ---

def teste_registrar_partida_valida():
    resetar_estado()
    r = partidas.registrar("Flamengo", "Vasco", 2, 1)
    passou = (
        r["status"] == 0
        and r["dados"]["time1"] == "Flamengo"
        and r["dados"]["time2"] == "Vasco"
        and r["dados"]["gols_time1"] == 2
        and r["dados"]["gols_time2"] == 1
    )
    registrar("registrar: partida válida retorna status 0 e dados corretos", passou, str(r))


def teste_registrar_com_rodada():
    resetar_estado()
    r = partidas.registrar("Flamengo", "Vasco", 3, 0, rodada=1)
    passou = r["status"] == 0 and r["dados"]["rodada"] == 1
    registrar("registrar: partida com rodada preserva o número da rodada", passou, str(r))


def teste_registrar_nome_vazio():
    resetar_estado()
    r = partidas.registrar("", "Vasco", 1, 0)
    passou = r["status"] == 1 and "Erro" in r["mensagem"]
    registrar("registrar: nome vazio retorna status 1 com mensagem de erro", passou, str(r))


def teste_registrar_mesmo_time():
    resetar_estado()
    r = partidas.registrar("Flamengo", "Flamengo", 1, 0)
    passou = r["status"] == 1 and "Erro" in r["mensagem"]
    registrar("registrar: mesmo time retorna status 1 com mensagem de erro", passou, str(r))


def teste_registrar_duplicata_na_rodada():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 2, 0, rodada=1)
    r = partidas.registrar("Flamengo", "Vasco", 1, 1, rodada=1)
    passou = r["status"] == 1 and "já foi registrada" in r["mensagem"]
    registrar("registrar: partida duplicada na mesma rodada retorna status 1", passou, str(r))


# --- listar ---

def teste_listar_sem_filtro():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0)
    partidas.registrar("Fluminense", "Botafogo", 2, 2)
    r = partidas.listar()
    passou = r["status"] == 0 and isinstance(r["dados"], list) and len(r["dados"]) == 2
    registrar("listar: sem filtro retorna status 0 e todas as partidas", passou, str(r))


def teste_listar_filtro_time():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0)
    partidas.registrar("Fluminense", "Botafogo", 2, 2)
    r = partidas.listar(filtro_time="Flamengo")
    lista = r["dados"]
    passou = (
        r["status"] == 0
        and len(lista) == 1
        and (lista[0]["time1"] == "Flamengo" or lista[0]["time2"] == "Flamengo")
    )
    registrar("listar: filtro por time retorna apenas partidas do time", passou, str(lista))


def teste_listar_filtro_rodada():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0, rodada=1)
    partidas.registrar("Fluminense", "Botafogo", 2, 2, rodada=2)
    r = partidas.listar(filtro_rodada=1)
    lista = r["dados"]
    passou = r["status"] == 0 and len(lista) == 1 and str(lista[0].get("rodada")) == "1"
    registrar("listar: filtro por rodada retorna apenas partidas da rodada", passou, str(lista))


def teste_listar_vazio():
    resetar_estado()
    r = partidas.listar()
    passou = r["status"] == 0 and r["dados"] == []
    registrar("listar: sem partidas retorna status 0 e lista vazia", passou, str(r))


# --- por_rodada ---

def teste_por_rodada_com_partidas():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0, rodada=1)
    partidas.registrar("Fluminense", "Botafogo", 2, 1, rodada=1)
    partidas.registrar("Palmeiras", "Santos", 0, 0, rodada=2)
    r = partidas.por_rodada(1)
    lista = r["dados"]
    passou = r["status"] == 0 and len(lista) == 2 and all(p.get("rodada") == 1 for p in lista)
    registrar("por_rodada: retorna status 0 e apenas as partidas da rodada informada", passou, str(lista))


def teste_por_rodada_inexistente():
    resetar_estado()
    r = partidas.por_rodada(99)
    passou = r["status"] == 0 and r["dados"] == []
    registrar("por_rodada: rodada sem partidas retorna status 0 e lista vazia", passou, str(r))


# --- rodadas ---

def teste_rodadas_com_dados():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0, rodada=1)
    partidas.registrar("Fluminense", "Botafogo", 2, 1, rodada=2)
    r = partidas.rodadas()
    passou = r["status"] == 0 and "1" in r["dados"] and "2" in r["dados"]
    registrar("rodadas: retorna status 0 e lista com as rodadas existentes", passou, str(r))


def teste_rodadas_ordenadas():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0, rodada=3)
    partidas.registrar("Fluminense", "Botafogo", 2, 1, rodada=1)
    r = partidas.rodadas()
    lista = r["dados"]
    passou = r["status"] == 0 and lista == sorted(lista)
    registrar("rodadas: lista retornada está em ordem crescente", passou, str(lista))


def teste_rodadas_sem_dados():
    resetar_estado()
    r = partidas.rodadas()
    passou = r["status"] == 0 and r["dados"] == []
    registrar("rodadas: sem partidas retorna status 0 e lista vazia", passou, str(r))


# --- inicializar / salvar ---

def teste_inicializar_retorna_dict():
    r = partidas.inicializar()
    passou = isinstance(r, dict) and "status" in r and "mensagem" in r and "dados" in r
    registrar("inicializar: retorna dict com status, mensagem e dados", passou, str(r))


def teste_salvar_retorna_status_zero():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0)
    r = partidas.salvar()
    passou = r["status"] == 0
    registrar("salvar: persiste dados e retorna status 0", passou, str(r))


# --- resetar ---

def teste_resetar_remove_todas_as_partidas():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0)
    partidas.registrar("Fluminense", "Botafogo", 2, 1)
    r = partidas.resetar()
    passou = r["status"] == 0 and partidas.listar()["dados"] == []
    registrar("resetar: sem argumento remove todas as partidas e retorna status 0", passou, str(r))


def teste_resetar_por_torneio():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0, rodada=1, torneio_id="t1")
    partidas.registrar("Fluminense", "Botafogo", 2, 1, rodada=1, torneio_id="t2")
    r = partidas.resetar(torneio_id="t1")
    lista_restante = partidas.listar()["dados"]
    passou = (
        r["status"] == 0
        and len(lista_restante) == 1
        and lista_restante[0].get("torneio_id") == "t2"
    )
    registrar("resetar: com torneio_id remove apenas partidas daquele torneio", passou, str(lista_restante))


# --- execução ---

def executar_testes():
    testes = [
        teste_registrar_partida_valida,
        teste_registrar_com_rodada,
        teste_registrar_nome_vazio,
        teste_registrar_mesmo_time,
        teste_registrar_duplicata_na_rodada,
        teste_listar_sem_filtro,
        teste_listar_filtro_time,
        teste_listar_filtro_rodada,
        teste_listar_vazio,
        teste_por_rodada_com_partidas,
        teste_por_rodada_inexistente,
        teste_rodadas_com_dados,
        teste_rodadas_ordenadas,
        teste_rodadas_sem_dados,
        teste_resetar_remove_todas_as_partidas,
        teste_resetar_por_torneio,
        teste_inicializar_retorna_dict,
        teste_salvar_retorna_status_zero,
    ]

    for teste in testes:
        try:
            teste()
        except Exception as e:
            nome = teste.__name__.replace("teste_", "").replace("_", " ")
            registrar(nome, False, f"Exceção: {e}")

    print("\nRelatório de Testes — partidas.py\n")
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
