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
    p = partidas.registrar("Flamengo", "Vasco", 2, 1)
    passou = (
        isinstance(p, dict)
        and p.get("time1") == "Flamengo"
        and p.get("time2") == "Vasco"
        and p.get("gols_time1") == 2
        and p.get("gols_time2") == 1
    )
    registrar("registrar: partida válida retorna dict com dados corretos", passou, str(p))


def teste_registrar_com_rodada():
    resetar_estado()
    p = partidas.registrar("Flamengo", "Vasco", 3, 0, rodada=1)
    passou = isinstance(p, dict) and p.get("rodada") == 1
    registrar("registrar: partida com rodada preserva o número da rodada", passou, str(p))


def teste_registrar_nome_vazio():
    resetar_estado()
    resultado = partidas.registrar("", "Vasco", 1, 0)
    passou = isinstance(resultado, str) and resultado.startswith("Erro")
    registrar("registrar: nome vazio retorna mensagem de erro", passou, str(resultado))


def teste_registrar_mesmo_time():
    resetar_estado()
    resultado = partidas.registrar("Flamengo", "Flamengo", 1, 0)
    passou = isinstance(resultado, str) and resultado.startswith("Erro")
    registrar("registrar: mesmo time retorna mensagem de erro", passou, str(resultado))


def teste_registrar_duplicata_na_rodada():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 2, 0, rodada=1)
    resultado = partidas.registrar("Flamengo", "Vasco", 1, 1, rodada=1)
    passou = isinstance(resultado, str) and "já foi registrada" in resultado
    registrar("registrar: partida duplicada na mesma rodada retorna mensagem de erro", passou, str(resultado))


# --- listar ---

def teste_listar_sem_filtro():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0)
    partidas.registrar("Fluminense", "Botafogo", 2, 2)
    lista = partidas.listar()
    passou = isinstance(lista, list) and len(lista) == 2
    registrar("listar: sem filtro retorna todas as partidas", passou, str(lista))


def teste_listar_filtro_time():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0)
    partidas.registrar("Fluminense", "Botafogo", 2, 2)
    lista = partidas.listar(filtro_time="Flamengo")
    passou = (
        len(lista) == 1
        and (lista[0]["time1"] == "Flamengo" or lista[0]["time2"] == "Flamengo")
    )
    registrar("listar: filtro por time retorna apenas partidas do time", passou, str(lista))


def teste_listar_filtro_rodada():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0, rodada=1)
    partidas.registrar("Fluminense", "Botafogo", 2, 2, rodada=2)
    lista = partidas.listar(filtro_rodada=1)
    passou = len(lista) == 1 and str(lista[0].get("rodada")) == "1"
    registrar("listar: filtro por rodada retorna apenas partidas da rodada", passou, str(lista))


def teste_listar_vazio():
    resetar_estado()
    lista = partidas.listar()
    passou = lista == []
    registrar("listar: sem partidas retorna lista vazia", passou, str(lista))


# --- por_rodada ---

def teste_por_rodada_com_partidas():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0, rodada=1)
    partidas.registrar("Fluminense", "Botafogo", 2, 1, rodada=1)
    partidas.registrar("Palmeiras", "Santos", 0, 0, rodada=2)
    lista = partidas.por_rodada(1)
    passou = len(lista) == 2 and all(p.get("rodada") == 1 for p in lista)
    registrar("por_rodada: retorna apenas as partidas da rodada informada", passou, str(lista))


def teste_por_rodada_inexistente():
    resetar_estado()
    lista = partidas.por_rodada(99)
    passou = lista == []
    registrar("por_rodada: rodada sem partidas retorna lista vazia", passou, str(lista))


# --- rodadas ---

def teste_rodadas_com_dados():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0, rodada=1)
    partidas.registrar("Fluminense", "Botafogo", 2, 1, rodada=2)
    r = partidas.rodadas()
    passou = isinstance(r, list) and "1" in r and "2" in r
    registrar("rodadas: retorna lista com as rodadas existentes", passou, str(r))


def teste_rodadas_ordenadas():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0, rodada=3)
    partidas.registrar("Fluminense", "Botafogo", 2, 1, rodada=1)
    r = partidas.rodadas()
    passou = r == sorted(r)
    registrar("rodadas: lista retornada está em ordem crescente", passou, str(r))


def teste_rodadas_sem_dados():
    resetar_estado()
    r = partidas.rodadas()
    passou = r == []
    registrar("rodadas: sem partidas retorna lista vazia", passou, str(r))


# --- inicializar / salvar ---

def teste_inicializar_retorna_inteiro():
    resultado = partidas.inicializar()
    passou = isinstance(resultado, int)
    registrar("inicializar: retorna int (0 se arquivo existe, 1 se não existe)", passou, str(resultado))


def teste_salvar_retorna_zero():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0)
    resultado = partidas.salvar()
    passou = resultado == 0
    registrar("salvar: persiste dados e retorna 0", passou, str(resultado))


# --- resetar ---

def teste_resetar_remove_todas_as_partidas():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0)
    partidas.registrar("Fluminense", "Botafogo", 2, 1)
    resultado = partidas.resetar()
    passou = resultado == 0 and partidas.listar() == []
    registrar("resetar: sem argumento remove todas as partidas", passou, str(partidas.listar()))


def teste_resetar_por_torneio():
    resetar_estado()
    partidas.registrar("Flamengo", "Vasco", 1, 0, rodada=1, torneio_id="t1")
    partidas.registrar("Fluminense", "Botafogo", 2, 1, rodada=1, torneio_id="t2")
    resultado = partidas.resetar(torneio_id="t1")
    lista_restante = partidas.listar()
    passou = (
        resultado == 0
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
        teste_inicializar_retorna_inteiro,
        teste_salvar_retorna_zero,
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
