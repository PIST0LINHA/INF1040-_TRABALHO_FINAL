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
    t = torneios.criar("Copa Teste", ["A", "B", "C", "D"])
    passou = (
        isinstance(t, dict)
        and t["nome"] == "Copa Teste"
        and t["times"] == ["A", "B", "C", "D"]
        and t["rodada"] == 1
        and t["campeao"] is None
        and len(t["confrontos"]) == 2
    )
    registrar("criar: retorna dict com dados do torneio criado", passou, str(t))


def teste_criar_nome_vazio_recebe_nome_padrao():
    resetar_estado()
    t = torneios.criar("", ["A", "B"])
    passou = isinstance(t, dict) and t["nome"].startswith("Torneio")
    registrar("criar: nome vazio recebe nome padrão", passou, str(t))


def teste_criar_numero_impar_de_times():
    resetar_estado()
    resultado = torneios.criar("Impar", ["A", "B", "C"])
    passou = isinstance(resultado, str) and resultado.startswith("Erro")
    registrar("criar: número ímpar de times retorna mensagem de erro", passou, str(resultado))


def teste_criar_menos_de_dois_times():
    resetar_estado()
    resultado = torneios.criar("Pequeno", ["A"])
    passou = isinstance(resultado, str) and resultado.startswith("Erro")
    registrar("criar: menos de 2 times retorna mensagem de erro", passou, str(resultado))


def teste_listar_retorna_todos_os_torneios():
    resetar_estado()
    torneios.criar("T1", ["A", "B"])
    torneios.criar("T2", ["C", "D"])
    lista = torneios.listar()
    passou = isinstance(lista, list) and len(lista) == 2
    registrar("listar: retorna todos os torneios criados", passou, str(lista))


def teste_listar_vazio():
    resetar_estado()
    passou = torneios.listar() == []
    registrar("listar: sem torneios retorna lista vazia", passou)


# --- get_ativo / set_ativo / desativar ---

def teste_criar_define_torneio_como_ativo():
    resetar_estado()
    t = torneios.criar("Ativo", ["A", "B"])
    ativo = torneios.get_ativo()
    passou = ativo is not None and ativo["id"] == t["id"]
    registrar("criar: define o torneio criado como ativo", passou, str(ativo))


def teste_set_ativo_torneio_existente():
    resetar_estado()
    t1 = torneios.criar("T1", ["A", "B"])
    torneios.criar("T2", ["C", "D"])
    resultado = torneios.set_ativo(t1["id"])
    passou = resultado == 0 and torneios.get_ativo()["id"] == t1["id"]
    registrar("set_ativo: torneio existente retorna 0 e torna-se ativo", passou, str(resultado))


def teste_set_ativo_torneio_inexistente():
    resetar_estado()
    resultado = torneios.set_ativo("id_invalido")
    passou = resultado == 1
    registrar("set_ativo: ID inexistente retorna 1", passou, str(resultado))


def teste_desativar_remove_ativo():
    resetar_estado()
    torneios.criar("T1", ["A", "B"])
    resultado = torneios.desativar()
    passou = resultado == 0 and torneios.get_ativo() is None
    registrar("desativar: retorna 0 e remove o torneio ativo", passou, str(resultado))


# --- get_confrontos / get_rodada / get_campeao ---

def teste_get_confrontos_retorna_lista_do_ativo():
    resetar_estado()
    torneios.criar("T1", ["A", "B"])
    confrontos = torneios.get_confrontos()
    passou = isinstance(confrontos, list) and len(confrontos) == 1
    registrar("get_confrontos: retorna confrontos do torneio ativo", passou, str(confrontos))


def teste_get_confrontos_sem_ativo_retorna_vazio():
    resetar_estado()
    passou = torneios.get_confrontos() == []
    registrar("get_confrontos: sem torneio ativo retorna lista vazia", passou)


def teste_get_rodada_retorna_rodada_atual():
    resetar_estado()
    torneios.criar("T1", ["A", "B"])
    passou = torneios.get_rodada() == 1
    registrar("get_rodada: retorna 1 na primeira rodada", passou, str(torneios.get_rodada()))


def teste_get_rodada_sem_ativo_retorna_zero():
    resetar_estado()
    passou = torneios.get_rodada() == 0
    registrar("get_rodada: sem torneio ativo retorna 0", passou, str(torneios.get_rodada()))


def teste_get_campeao_sem_campeao_retorna_none():
    resetar_estado()
    torneios.criar("T1", ["A", "B"])
    passou = torneios.get_campeao() is None
    registrar("get_campeao: sem campeão definido retorna None", passou, str(torneios.get_campeao()))


# --- confrontos_pendentes / rodada_completa ---

def teste_confrontos_pendentes_sem_resultados():
    resetar_estado()
    torneios.criar("T1", ["A", "B"])
    pendentes = torneios.confrontos_pendentes()
    passou = isinstance(pendentes, list) and len(pendentes) == 1
    registrar("confrontos_pendentes: retorna confrontos sem resultado registrado", passou, str(pendentes))


def teste_rodada_completa_falso_sem_resultados():
    resetar_estado()
    torneios.criar("T1", ["A", "B"])
    passou = torneios.rodada_completa() is False
    registrar("rodada_completa: retorna False sem resultados registrados", passou)


def teste_rodada_completa_verdadeiro_apos_registrar():
    resetar_estado()
    t = torneios.criar("T1", ["A", "B"])
    c = torneios.get_confrontos()[0]
    partidas.registrar(c[0], c[1], 1, 0, rodada=1, torneio_id=t["id"])
    passou = torneios.rodada_completa() is True
    registrar("rodada_completa: retorna True após registrar todos os resultados", passou)


# --- resetar_ativo ---

def teste_resetar_ativo_reinicia_torneio():
    resetar_estado()
    t = torneios.criar("T1", ["A", "B"])
    c = torneios.get_confrontos()[0]
    partidas.registrar(c[0], c[1], 2, 0, rodada=1, torneio_id=t["id"])
    resultado = torneios.resetar_ativo()
    passou = (
        resultado == 0
        and torneios.get_rodada() == 1
        and torneios.get_campeao() is None
    )
    registrar("resetar_ativo: reinicia rodada e campeão do torneio ativo", passou, str(resultado))


def teste_resetar_ativo_sem_ativo_retorna_um():
    resetar_estado()
    passou = torneios.resetar_ativo() == 1
    registrar("resetar_ativo: sem torneio ativo retorna 1", passou)


# --- inicializar / salvar ---

def teste_inicializar_retorna_inteiro():
    resultado = torneios.inicializar()
    passou = isinstance(resultado, int)
    registrar("inicializar: retorna int (0 se arquivo existe, 1 se não existe)", passou, str(resultado))


def teste_salvar_retorna_zero():
    resetar_estado()
    torneios.criar("T_salvar", ["A", "B"])
    resultado = torneios.salvar()
    passou = resultado == 0
    registrar("salvar: persiste dados e retorna 0", passou, str(resultado))


# --- get_ativo ---

def teste_get_ativo_retorna_dict_quando_ativo():
    resetar_estado()
    t = torneios.criar("T_ativo", ["A", "B"])
    ativo = torneios.get_ativo()
    passou = isinstance(ativo, dict) and ativo["id"] == t["id"]
    registrar("get_ativo: retorna dict do torneio ativo", passou, str(ativo))


def teste_get_ativo_retorna_none_sem_ativo():
    resetar_estado()
    passou = torneios.get_ativo() is None
    registrar("get_ativo: sem torneio ativo retorna None", passou)


# --- eh_confronto_ativo ---

def teste_eh_confronto_ativo_verdadeiro():
    resetar_estado()
    torneios.criar("T_conf", ["A", "B"])
    c = torneios.get_confrontos()[0]
    passou = torneios.eh_confronto_ativo(c[0], c[1]) is True
    registrar("eh_confronto_ativo: par válido retorna True", passou, str(c))


def teste_eh_confronto_ativo_falso():
    resetar_estado()
    torneios.criar("T_conf2", ["A", "B"])
    passou = torneios.eh_confronto_ativo("X", "Y") is False
    registrar("eh_confronto_ativo: par inválido retorna False", passou)


def teste_eh_confronto_ativo_sem_torneio():
    resetar_estado()
    passou = torneios.eh_confronto_ativo("A", "B") is False
    registrar("eh_confronto_ativo: sem torneio ativo retorna False", passou)


# --- contexto_partida ---

def teste_contexto_partida_confronto_ativo():
    resetar_estado()
    t = torneios.criar("T_ctx", ["A", "B"])
    c = torneios.get_confrontos()[0]
    torneio_id, rodada = torneios.contexto_partida(c[0], c[1])
    passou = torneio_id == t["id"] and rodada == 1
    registrar("contexto_partida: confronto ativo retorna (torneio_id, rodada)", passou,
              str((torneio_id, rodada)))


def teste_contexto_partida_sem_confronto():
    resetar_estado()
    torneios.criar("T_ctx2", ["A", "B"])
    torneio_id, rodada = torneios.contexto_partida("X", "Y")
    passou = torneio_id is None and rodada is None
    registrar("contexto_partida: par não é confronto ativo retorna (None, None)", passou,
              str((torneio_id, rodada)))


def teste_contexto_partida_sem_torneio():
    resetar_estado()
    torneio_id, rodada = torneios.contexto_partida("A", "B")
    passou = torneio_id is None and rodada is None
    registrar("contexto_partida: sem torneio ativo retorna (None, None)", passou,
              str((torneio_id, rodada)))


# --- avancar ---

def teste_avancar_sem_torneio_ativo_retorna_um():
    resetar_estado()
    passou = torneios.avancar() == 1
    registrar("avancar: sem torneio ativo retorna 1", passou)


def teste_avancar_define_campeao():
    resetar_estado()
    t = torneios.criar("Final", ["A", "B"])
    c = torneios.get_confrontos()[0]
    partidas.registrar(c[0], c[1], 2, 0, rodada=1, torneio_id=t["id"])
    resultado = torneios.avancar()
    passou = resultado == 0 and torneios.get_campeao() == c[0]
    registrar("avancar: define campeão quando resta 1 time classificado", passou,
              str(torneios.get_campeao()))


def teste_avancar_proxima_rodada():
    resetar_estado()
    t = torneios.criar("Semi", ["A", "B", "C", "D"])
    for c in torneios.get_confrontos():
        partidas.registrar(c[0], c[1], 2, 0, rodada=1, torneio_id=t["id"])
    resultado = torneios.avancar()
    passou = (
        resultado == 0
        and torneios.get_rodada() == 2
        and len(torneios.get_confrontos()) == 1
    )
    registrar("avancar: com 4 times avança para rodada 2 com 1 confronto", passou,
              str(torneios.get_rodada()))


# --- resetar ---

def teste_resetar_remove_todos_torneios():
    resetar_estado()
    torneios.criar("T1", ["A", "B"])
    torneios.criar("T2", ["C", "D"])
    resultado = torneios.resetar()
    passou = resultado == 0 and torneios.listar() == [] and torneios.get_ativo() is None
    registrar("resetar: remove todos os torneios e limpa o ativo", passou, str(torneios.listar()))


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
        teste_get_confrontos_retorna_lista_do_ativo,
        teste_get_confrontos_sem_ativo_retorna_vazio,
        teste_get_rodada_retorna_rodada_atual,
        teste_get_rodada_sem_ativo_retorna_zero,
        teste_get_campeao_sem_campeao_retorna_none,
        teste_confrontos_pendentes_sem_resultados,
        teste_rodada_completa_falso_sem_resultados,
        teste_rodada_completa_verdadeiro_apos_registrar,
        teste_resetar_ativo_reinicia_torneio,
        teste_resetar_ativo_sem_ativo_retorna_um,
        teste_avancar_sem_torneio_ativo_retorna_um,
        teste_avancar_define_campeao,
        teste_avancar_proxima_rodada,
        teste_resetar_remove_todos_torneios,
        teste_inicializar_retorna_inteiro,
        teste_salvar_retorna_zero,
        teste_get_ativo_retorna_dict_quando_ativo,
        teste_get_ativo_retorna_none_sem_ativo,
        teste_eh_confronto_ativo_verdadeiro,
        teste_eh_confronto_ativo_falso,
        teste_eh_confronto_ativo_sem_torneio,
        teste_contexto_partida_confronto_ativo,
        teste_contexto_partida_sem_confronto,
        teste_contexto_partida_sem_torneio,
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
