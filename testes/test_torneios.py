import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import torneios, partidas

resultados = []


def registrar(nome_teste, passou, detalhe=""):
    resultados.append({"teste": nome_teste, "passou": passou, "detalhe": detalhe})


def resetar_estado():
    torneios.resetar()
    partidas.resetar()


# --- criar / listar ---

def teste_criar_retorna_dict_com_dados():
    resetar_estado()
    r = torneios.criar("Copa Teste", ["A", "B", "C", "D"])
    dados = r["dados"]
    passou = (
        r["status"] == 0
        and dados["nome"] == "Copa Teste"
        and dados["times"] == ["A", "B", "C", "D"]
        and dados["rodada"] == 1
        and dados["campeao"] is None
        and len(dados["confrontos"]) == 2
    )
    registrar("criar: retorna status 0 e dados do torneio criado", passou, str(r))


def teste_criar_nome_vazio_recebe_nome_padrao():
    resetar_estado()
    r = torneios.criar("", ["A", "B"])
    passou = r["status"] == 0 and r["dados"]["nome"].startswith("Torneio")
    registrar("criar: nome vazio recebe nome padrão e retorna status 0", passou, str(r))


def teste_criar_numero_impar_de_times():
    resetar_estado()
    r = torneios.criar("Impar", ["A", "B", "C"])
    passou = r["status"] == 1 and "Erro" in r["mensagem"]
    registrar("criar: número ímpar de times retorna status 1 com mensagem de erro", passou, str(r))


def teste_criar_menos_de_dois_times():
    resetar_estado()
    r = torneios.criar("Pequeno", ["A"])
    passou = r["status"] == 1 and "Erro" in r["mensagem"]
    registrar("criar: menos de 2 times retorna status 1 com mensagem de erro", passou, str(r))


def teste_listar_retorna_todos_os_torneios():
    resetar_estado()
    torneios.criar("T1", ["A", "B"])
    torneios.criar("T2", ["C", "D"])
    r = torneios.listar()
    passou = r["status"] == 0 and isinstance(r["dados"], list) and len(r["dados"]) == 2
    registrar("listar: retorna status 0 e todos os torneios criados", passou, str(r))


def teste_listar_vazio():
    resetar_estado()
    r = torneios.listar()
    passou = r["status"] == 0 and r["dados"] == []
    registrar("listar: sem torneios retorna status 0 e lista vazia", passou, str(r))


# --- get_ativo / set_ativo / desativar ---

def teste_criar_define_torneio_como_ativo():
    resetar_estado()
    t = torneios.criar("Ativo", ["A", "B"])
    ativo = torneios.get_ativo()["dados"]
    passou = ativo is not None and ativo["id"] == t["dados"]["id"]
    registrar("criar: define o torneio criado como ativo", passou, str(ativo))


def teste_set_ativo_torneio_existente():
    resetar_estado()
    t1 = torneios.criar("T1", ["A", "B"])
    torneios.criar("T2", ["C", "D"])
    r = torneios.set_ativo(t1["dados"]["id"])
    passou = r["status"] == 0 and torneios.get_ativo()["dados"]["id"] == t1["dados"]["id"]
    registrar("set_ativo: torneio existente retorna status 0 e torna-se ativo", passou, str(r))


def teste_set_ativo_torneio_inexistente():
    resetar_estado()
    r = torneios.set_ativo("id_invalido")
    passou = r["status"] == 1
    registrar("set_ativo: ID inexistente retorna status 1", passou, str(r))


def teste_desativar_remove_ativo():
    resetar_estado()
    torneios.criar("T1", ["A", "B"])
    r = torneios.desativar()
    passou = r["status"] == 0 and torneios.get_ativo()["dados"] is None
    registrar("desativar: retorna status 0 e remove o torneio ativo", passou, str(r))


# --- get_ativo campos: confrontos / rodada / campeao ---

def teste_get_ativo_confrontos_retorna_lista_do_ativo():
    resetar_estado()
    torneios.criar("T1", ["A", "B"])
    ativo = torneios.get_ativo()["dados"]
    confrontos = ativo["confrontos"] if ativo else []
    passou = isinstance(confrontos, list) and len(confrontos) == 1
    registrar("get_ativo: campo confrontos retorna lista do torneio ativo", passou, str(confrontos))


def teste_get_ativo_none_confrontos_vazio():
    resetar_estado()
    ativo = torneios.get_ativo()["dados"]
    confrontos = ativo["confrontos"] if ativo else []
    passou = confrontos == []
    registrar("get_ativo: sem torneio ativo resulta em confrontos vazio", passou)


def teste_get_ativo_rodada_retorna_rodada_atual():
    resetar_estado()
    torneios.criar("T1", ["A", "B"])
    ativo = torneios.get_ativo()["dados"]
    passou = ativo is not None and ativo["rodada"] == 1
    registrar("get_ativo: campo rodada retorna 1 na primeira rodada", passou, str(ativo))


def teste_get_ativo_none_rodada_zero():
    resetar_estado()
    ativo = torneios.get_ativo()["dados"]
    rodada = ativo["rodada"] if ativo else 0
    passou = rodada == 0
    registrar("get_ativo: sem torneio ativo resulta em rodada 0", passou, str(rodada))


def teste_get_ativo_campeao_sem_campeao_retorna_none():
    resetar_estado()
    torneios.criar("T1", ["A", "B"])
    ativo = torneios.get_ativo()["dados"]
    passou = ativo is not None and ativo["campeao"] is None
    registrar("get_ativo: campo campeao sem campeão definido retorna None", passou, str(ativo))


# --- confrontos_pendentes ---

def teste_confrontos_pendentes_sem_resultados():
    resetar_estado()
    torneios.criar("T1", ["A", "B"])
    r = torneios.confrontos_pendentes()
    pendentes = r["dados"]
    passou = r["status"] == 0 and isinstance(pendentes, list) and len(pendentes) == 1
    registrar("confrontos_pendentes: retorna status 0 e confrontos sem resultado", passou, str(r))


def teste_confrontos_pendentes_falso_sem_resultados():
    resetar_estado()
    torneios.criar("T1", ["A", "B"])
    r = torneios.confrontos_pendentes()
    passou = r["status"] == 0 and len(r["dados"]) > 0
    registrar("confrontos_pendentes: lista não vazia sem resultados registrados", passou, str(r))


def teste_confrontos_pendentes_vazio_apos_registrar():
    resetar_estado()
    t = torneios.criar("T1", ["A", "B"])
    ativo = torneios.get_ativo()["dados"]
    c = ativo["confrontos"][0]
    partidas.registrar(c[0], c[1], 1, 0, rodada=1, torneio_id=t["dados"]["id"])
    r = torneios.confrontos_pendentes()
    passou = r["status"] == 0 and r["dados"] == []
    registrar("confrontos_pendentes: retorna status 0 e lista vazia após registrar todos", passou, str(r))


def teste_confrontos_pendentes_sem_torneio_ativo():
    resetar_estado()
    r = torneios.confrontos_pendentes()
    passou = r["status"] == 1 and r["dados"] is None
    registrar("confrontos_pendentes: sem torneio ativo retorna status 1 e dados None", passou, str(r))


# --- resetar_ativo ---

def teste_resetar_ativo_reinicia_torneio():
    resetar_estado()
    t = torneios.criar("T1", ["A", "B"])
    ativo = torneios.get_ativo()["dados"]
    c = ativo["confrontos"][0]
    partidas.registrar(c[0], c[1], 2, 0, rodada=1, torneio_id=t["dados"]["id"])
    r = torneios.resetar_ativo()
    ativo = torneios.get_ativo()["dados"]
    passou = (
        r["status"] == 0
        and ativo["rodada"] == 1
        and ativo["campeao"] is None
    )
    registrar("resetar_ativo: reinicia rodada e campeão do torneio ativo", passou, str(r))


def teste_resetar_ativo_sem_ativo_retorna_status_um():
    resetar_estado()
    r = torneios.resetar_ativo()
    passou = r["status"] == 1
    registrar("resetar_ativo: sem torneio ativo retorna status 1", passou, str(r))


# --- inicializar / salvar ---

def teste_inicializar_retorna_dict():
    r = torneios.inicializar()
    passou = isinstance(r, dict) and "status" in r and "mensagem" in r and "dados" in r
    registrar("inicializar: retorna dict com status, mensagem e dados", passou, str(r))


def teste_salvar_retorna_status_zero():
    resetar_estado()
    torneios.criar("T_salvar", ["A", "B"])
    r = torneios.salvar()
    passou = r["status"] == 0
    registrar("salvar: persiste dados e retorna status 0", passou, str(r))


# --- get_ativo ---

def teste_get_ativo_retorna_dados_quando_ativo():
    resetar_estado()
    t = torneios.criar("T_ativo", ["A", "B"])
    r = torneios.get_ativo()
    passou = r["status"] == 0 and r["dados"]["id"] == t["dados"]["id"]
    registrar("get_ativo: retorna status 0 e dados do torneio ativo", passou, str(r))


def teste_get_ativo_retorna_status_um_sem_ativo():
    resetar_estado()
    r = torneios.get_ativo()
    passou = r["status"] == 1 and r["dados"] is None
    registrar("get_ativo: sem torneio ativo retorna status 1 e dados None", passou, str(r))


# --- contexto_partida ---

def teste_contexto_partida_par_valido_retorna_dados():
    resetar_estado()
    torneios.criar("T_conf", ["A", "B"])
    ativo = torneios.get_ativo()["dados"]
    c = ativo["confrontos"][0]
    r = torneios.contexto_partida(c[0], c[1])
    torneio_id, rodada = r["dados"]
    passou = r["status"] == 0 and torneio_id is not None and rodada is not None
    registrar("contexto_partida: par válido retorna status 0 e (torneio_id, rodada)", passou, str(r))


def teste_contexto_partida_par_invalido_retorna_status_um():
    resetar_estado()
    torneios.criar("T_conf2", ["A", "B"])
    r = torneios.contexto_partida("X", "Y")
    torneio_id, rodada = r["dados"]
    passou = r["status"] == 1 and torneio_id is None and rodada is None
    registrar("contexto_partida: par inválido retorna status 1 e (None, None)", passou, str(r))


def teste_contexto_partida_sem_torneio_retorna_status_um():
    resetar_estado()
    r = torneios.contexto_partida("A", "B")
    torneio_id, rodada = r["dados"]
    passou = r["status"] == 1 and torneio_id is None and rodada is None
    registrar("contexto_partida: sem torneio ativo retorna status 1 e (None, None)", passou, str(r))


def teste_contexto_partida_confronto_ativo():
    resetar_estado()
    t = torneios.criar("T_ctx", ["A", "B"])
    ativo = torneios.get_ativo()["dados"]
    c = ativo["confrontos"][0]
    r = torneios.contexto_partida(c[0], c[1])
    torneio_id, rodada = r["dados"]
    passou = r["status"] == 0 and torneio_id == t["dados"]["id"] and rodada == 1
    registrar("contexto_partida: confronto ativo retorna status 0 e (torneio_id, rodada)", passou, str(r))


def teste_contexto_partida_sem_confronto():
    resetar_estado()
    torneios.criar("T_ctx2", ["A", "B"])
    r = torneios.contexto_partida("X", "Y")
    torneio_id, rodada = r["dados"]
    passou = r["status"] == 1 and torneio_id is None and rodada is None
    registrar("contexto_partida: par não é confronto ativo retorna status 1", passou, str(r))


# --- avancar ---

def teste_avancar_sem_torneio_ativo_retorna_status_um():
    resetar_estado()
    r = torneios.avancar()
    passou = r["status"] == 1
    registrar("avancar: sem torneio ativo retorna status 1", passou, str(r))


def teste_avancar_define_campeao():
    resetar_estado()
    t = torneios.criar("Final", ["A", "B"])
    ativo = torneios.get_ativo()["dados"]
    c = ativo["confrontos"][0]
    partidas.registrar(c[0], c[1], 2, 0, rodada=1, torneio_id=t["dados"]["id"])
    r = torneios.avancar()
    ativo = torneios.get_ativo()["dados"]
    passou = r["status"] == 0 and ativo["campeao"] == c[0]
    registrar("avancar: define campeão quando resta 1 time classificado", passou,
              str(ativo["campeao"] if ativo else None))


def teste_avancar_proxima_rodada():
    resetar_estado()
    t = torneios.criar("Semi", ["A", "B", "C", "D"])
    ativo = torneios.get_ativo()["dados"]
    for c in ativo["confrontos"]:
        partidas.registrar(c[0], c[1], 2, 0, rodada=1, torneio_id=t["dados"]["id"])
    r = torneios.avancar()
    ativo = torneios.get_ativo()["dados"]
    passou = (
        r["status"] == 0
        and ativo["rodada"] == 2
        and len(ativo["confrontos"]) == 1
    )
    registrar("avancar: com 4 times avança para rodada 2 com 1 confronto", passou,
              str(ativo["rodada"] if ativo else None))


# --- resetar ---

def teste_resetar_remove_todos_torneios():
    resetar_estado()
    torneios.criar("T1", ["A", "B"])
    torneios.criar("T2", ["C", "D"])
    r = torneios.resetar()
    passou = r["status"] == 0 and torneios.listar()["dados"] == [] and torneios.get_ativo()["dados"] is None
    registrar("resetar: remove todos os torneios e limpa o ativo", passou, str(r))


# --- execução ---

def executar_testes():
    testes = [
        teste_criar_retorna_dict_com_dados,
        teste_criar_nome_vazio_recebe_nome_padrao,
        teste_criar_numero_impar_de_times,
        teste_criar_menos_de_dois_times,
        teste_listar_retorna_todos_os_torneios,
        teste_listar_vazio,
        teste_criar_define_torneio_como_ativo,
        teste_set_ativo_torneio_existente,
        teste_set_ativo_torneio_inexistente,
        teste_desativar_remove_ativo,
        teste_get_ativo_confrontos_retorna_lista_do_ativo,
        teste_get_ativo_none_confrontos_vazio,
        teste_get_ativo_rodada_retorna_rodada_atual,
        teste_get_ativo_none_rodada_zero,
        teste_get_ativo_campeao_sem_campeao_retorna_none,
        teste_confrontos_pendentes_sem_resultados,
        teste_confrontos_pendentes_falso_sem_resultados,
        teste_confrontos_pendentes_vazio_apos_registrar,
        teste_confrontos_pendentes_sem_torneio_ativo,
        teste_resetar_ativo_reinicia_torneio,
        teste_resetar_ativo_sem_ativo_retorna_status_um,
        teste_avancar_sem_torneio_ativo_retorna_status_um,
        teste_avancar_define_campeao,
        teste_avancar_proxima_rodada,
        teste_resetar_remove_todos_torneios,
        teste_inicializar_retorna_dict,
        teste_salvar_retorna_status_zero,
        teste_get_ativo_retorna_dados_quando_ativo,
        teste_get_ativo_retorna_status_um_sem_ativo,
        teste_contexto_partida_par_valido_retorna_dados,
        teste_contexto_partida_par_invalido_retorna_status_um,
        teste_contexto_partida_sem_torneio_retorna_status_um,
        teste_contexto_partida_confronto_ativo,
        teste_contexto_partida_sem_confronto,
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
