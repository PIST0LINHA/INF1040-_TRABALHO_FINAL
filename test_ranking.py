import ranking

resultados = []


def registrar(nome_teste, passou, detalhe=""):
    resultados.append({"teste": nome_teste, "passou": passou, "detalhe": detalhe})


def resetar():
    ranking.criar_tabela(['Flamengo', 'Vasco', 'Fluminense', 'Botafogo'])


# ==================== criar_tabela ====================

def teste_criar_tabela_multiplos_times():
    ranking.criar_tabela(['Flamengo', 'Vasco', 'Fluminense'])
    relacao = ranking.ordenar_classificacao()
    passou = (
        len(relacao) == 3
        and all(t['pontos'] == 0 for t in relacao)
        and all(t['vitorias'] == 0 for t in relacao)
        and all(t['empates'] == 0 for t in relacao)
        and all(t['derrotas'] == 0 for t in relacao)
        and all(t['gols_pro'] == 0 for t in relacao)
        and all(t['gols_contra'] == 0 for t in relacao)
    )
    registrar("criar_tabela: múltiplos times com contadores zerados", passou, str(relacao))


def teste_criar_tabela_nome_preservado():
    ranking.criar_tabela(['Flamengo'])
    relacao = ranking.ordenar_classificacao()
    passou = relacao[0]['time'] == 'Flamengo'
    registrar("criar_tabela: nome do time preservado", passou, str(relacao))


def teste_criar_tabela_lista_vazia():
    ranking.criar_tabela([])
    relacao = ranking.ordenar_classificacao()
    passou = relacao == []
    registrar("criar_tabela: lista vazia não gera erro", passou, str(relacao))


# ==================== atualizar_pontos ====================

def teste_atualizar_pontos_vitoria_time1():
    ranking.criar_tabela(['Flamengo', 'Vasco'])
    ranking.atualizar_pontos({'time1': 'Flamengo', 'gols_time1': 2,
                               'time2': 'Vasco',    'gols_time2': 0})
    relacao  = ranking.ordenar_classificacao()
    flamengo = next(t for t in relacao if t['time'] == 'Flamengo')
    vasco    = next(t for t in relacao if t['time'] == 'Vasco')
    passou = (
        flamengo['pontos'] == 3 and flamengo['vitorias'] == 1 and flamengo['derrotas'] == 0
        and vasco['pontos'] == 0 and vasco['vitorias'] == 0 and vasco['derrotas'] == 1
    )
    registrar("atualizar_pontos: vitória do time da casa", passou,
              f"Flamengo={flamengo} | Vasco={vasco}")


def teste_atualizar_pontos_vitoria_time_fora():
    ranking.criar_tabela(['Flamengo', 'Vasco'])
    ranking.atualizar_pontos({'time1': 'Flamengo', 'gols_time1': 0,
                               'time2': 'Vasco',    'gols_time2': 7})
    relacao  = ranking.ordenar_classificacao()
    flamengo = next(t for t in relacao if t['time'] == 'Flamengo')
    vasco    = next(t for t in relacao if t['time'] == 'Vasco')
    passou = (
        vasco['pontos'] == 3 and vasco['vitorias'] == 1 and vasco['derrotas'] == 0
        and flamengo['pontos'] == 0 and flamengo['vitorias'] == 0 and flamengo['derrotas'] == 1
    )
    registrar("atualizar_pontos: vitória do time de fora", passou,
              f"Flamengo={flamengo} | Vasco={vasco}")


def teste_atualizar_pontos_empate():
    ranking.criar_tabela(['Flamengo', 'Vasco'])
    ranking.atualizar_pontos({'time1': 'Flamengo', 'gols_time1': 1,
                               'time2': 'Vasco',    'gols_time2': 1})
    relacao  = ranking.ordenar_classificacao()
    flamengo = next(t for t in relacao if t['time'] == 'Flamengo')
    vasco    = next(t for t in relacao if t['time'] == 'Vasco')
    passou = (
        flamengo['pontos'] == 1 and flamengo['empates'] == 1
        and vasco['pontos'] == 1 and vasco['empates'] == 1
    )
    registrar("atualizar_pontos: empate", passou,
              f"Flamengo={flamengo} | Vasco={vasco}")


def teste_atualizar_pontos_gols_contabilizados():
    ranking.criar_tabela(['Flamengo', 'Vasco'])
    ranking.atualizar_pontos({'time1': 'Flamengo', 'gols_time1': 3,
                               'time2': 'Vasco',    'gols_time2': 1})
    relacao  = ranking.ordenar_classificacao()
    flamengo = next(t for t in relacao if t['time'] == 'Flamengo')
    vasco    = next(t for t in relacao if t['time'] == 'Vasco')
    passou = (
        flamengo['gols_pro'] == 3 and flamengo['gols_contra'] == 1
        and vasco['gols_pro'] == 1 and vasco['gols_contra'] == 3
    )
    registrar("atualizar_pontos: gols contabilizados corretamente", passou,
              f"Flamengo={flamengo} | Vasco={vasco}")


def teste_atualizar_pontos_acumulativo():
    ranking.criar_tabela(['Flamengo', 'Vasco'])
    ranking.atualizar_pontos({'time1': 'Flamengo', 'gols_time1': 2,
                               'time2': 'Vasco',    'gols_time2': 0})
    ranking.atualizar_pontos({'time1': 'Flamengo', 'gols_time1': 1,
                               'time2': 'Vasco',    'gols_time2': 1})
    relacao  = ranking.ordenar_classificacao()
    flamengo = next(t for t in relacao if t['time'] == 'Flamengo')
    passou = (
        flamengo['pontos'] == 4
        and flamengo['vitorias'] == 1
        and flamengo['empates'] == 1
        and flamengo['gols_pro'] == 3
        and flamengo['gols_contra'] == 1
    )
    registrar("atualizar_pontos: acumulativo após 2 partidas", passou, str(flamengo))


# ==================== ordenar_classificacao ====================

def teste_ordenar_classificacao_por_pontos():
    ranking.criar_tabela(['Flamengo', 'Vasco', 'Fluminense'])
    # fluminense venceu os 3 jogos - 9 pts
    ranking.atualizar_pontos({'time1': 'Fluminense', 'gols_time1': 1, 'time2': 'Flamengo', 'gols_time2': 0})
    ranking.atualizar_pontos({'time1': 'Fluminense', 'gols_time1': 1, 'time2': 'Vasco',    'gols_time2': 0})
    ranking.atualizar_pontos({'time1': 'Fluminense', 'gols_time1': 1, 'time2': 'Vasco',    'gols_time2': 0})
    # flamengo venceu 2 jogos - 6 pts
    ranking.atualizar_pontos({'time1': 'Flamengo', 'gols_time1': 1, 'time2': 'Vasco', 'gols_time2': 0})
    ranking.atualizar_pontos({'time1': 'Flamengo', 'gols_time1': 1, 'time2': 'Vasco', 'gols_time2': 0})
    # vasco venceu 1 jogo - 3 pts
    ranking.atualizar_pontos({'time1': 'Vasco', 'gols_time1': 1, 'time2': 'Flamengo', 'gols_time2': 0})
    relacao = ranking.ordenar_classificacao()
    passou = (
        relacao[0]['time'] == 'Fluminense'
        and relacao[1]['time'] == 'Flamengo'
        and relacao[2]['time'] == 'Vasco'
    )
    registrar("ordenar_classificacao: ordenação por pontos", passou, str(relacao))


def teste_ordenar_classificacao_desempate_vitorias():
    ranking.criar_tabela(['Flamengo', 'Vasco'])
    ranking.atualizar_pontos({'time1': 'Flamengo', 'gols_time1': 1,
                               'time2': 'Vasco',    'gols_time2': 0})
    relacao = ranking.ordenar_classificacao()
    passou = (
        relacao[0]['time'] == 'Flamengo' and relacao[0]['vitorias'] == 1
        and relacao[1]['time'] == 'Vasco' and relacao[1]['vitorias'] == 0
    )
    registrar("ordenar_classificacao: desempate por vitórias", passou, str(relacao))


def teste_ordenar_classificacao_desempate_saldo_gols():
    ranking.criar_tabela(['Flamengo', 'Vasco', 'Fluminense'])
    ranking.atualizar_pontos({'time1': 'Flamengo',   'gols_time1': 3,
                               'time2': 'Fluminense', 'gols_time2': 1})
    ranking.atualizar_pontos({'time1': 'Vasco',      'gols_time1': 2,
                               'time2': 'Fluminense', 'gols_time2': 1})
    relacao  = ranking.ordenar_classificacao()
    flamengo = next(t for t in relacao if t['time'] == 'Flamengo')
    vasco    = next(t for t in relacao if t['time'] == 'Vasco')
    passou = relacao.index(flamengo) < relacao.index(vasco)
    registrar("ordenar_classificacao: desempate por saldo de gols", passou, str(relacao))


def teste_ordenar_classificacao_tabela_original_nao_modificada():
    ranking.criar_tabela(['Flamengo', 'Vasco'])
    ranking.atualizar_pontos({'time1': 'Vasco',    'gols_time1': 3,
                               'time2': 'Flamengo', 'gols_time2': 0})
    relacao_antes = ranking.ordenar_classificacao()
    primeiro_antes = relacao_antes[0]['time']
    ranking.ordenar_classificacao()
    relacao_depois = ranking.ordenar_classificacao()
    passou = relacao_depois[0]['time'] == primeiro_antes
    registrar("ordenar_classificacao: tabela original não modificada", passou,
              f"antes={primeiro_antes} | depois={relacao_depois[0]['time']}")


# ==================== mostrar_classificacao ====================

def teste_mostrar_classificacao_condicao_retorno():
    ranking.criar_tabela(['Flamengo', 'Vasco'])
    retorno = ranking.mostrar_classificacao()
    passou = retorno == 0
    registrar("mostrar_classificacao: retorna 0 com sucesso", passou, str(retorno))


def teste_mostrar_classificacao_tabela_nao_modificada():
    ranking.criar_tabela(['Flamengo', 'Vasco'])
    ranking.atualizar_pontos({'time1': 'Flamengo', 'gols_time1': 2,
                               'time2': 'Vasco',    'gols_time2': 0})
    ranking.mostrar_classificacao()
    relacao  = ranking.ordenar_classificacao()
    flamengo = next(t for t in relacao if t['time'] == 'Flamengo')
    vasco    = next(t for t in relacao if t['time'] == 'Vasco')
    passou = flamengo['pontos'] == 3 and vasco['pontos'] == 0
    registrar("mostrar_classificacao: tabela não modificada após exibição", passou,
              f"Flamengo={flamengo['pontos']} pts | Vasco={vasco['pontos']} pts")


def teste_mostrar_classificacao_tabela_vazia():
    ranking.criar_tabela([])
    try:
        ranking.mostrar_classificacao()
        passou = True
    except Exception as e:
        passou = False
    registrar("mostrar_classificacao: tabela vazia não gera erro", passou)
    resetar()


# ==================== EXECUÇÃO ====================

def executar_testes():
    testes = [
        teste_criar_tabela_multiplos_times,
        teste_criar_tabela_nome_preservado,
        teste_criar_tabela_lista_vazia,
        teste_atualizar_pontos_vitoria_time1,
        teste_atualizar_pontos_vitoria_time_fora,
        teste_atualizar_pontos_empate,
        teste_atualizar_pontos_gols_contabilizados,
        teste_atualizar_pontos_acumulativo,
        teste_ordenar_classificacao_por_pontos,
        teste_ordenar_classificacao_desempate_vitorias,
        teste_ordenar_classificacao_desempate_saldo_gols,
        teste_ordenar_classificacao_tabela_original_nao_modificada,
        teste_mostrar_classificacao_condicao_retorno,
        teste_mostrar_classificacao_tabela_nao_modificada,
        teste_mostrar_classificacao_tabela_vazia,
    ]

    for teste in testes:
        try:
            teste()
        except Exception as e:
            nome = teste.__name__.replace("teste_", "").replace("_", " ")
            registrar(nome, False, f"Exceção: {e}")

    print("\nRelatório de Testes - ranking.py\n")
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