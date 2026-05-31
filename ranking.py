__all__ = ["criar_tabela", "atualizar_pontos", "ordenar_classificacao", "mostrar_classificacao"]

_tabela = []

def criar_tabela(lista_times: list[str]) -> int:
    _tabela.clear() 
    for time in lista_times:
        _tabela.append({
            'time': time,
            'pontos': 0,
            'jogos': 0,
            'vitorias': 0,
            'empates': 0,
            'derrotas': 0,
            'gols_pro': 0,
            'gols_contra': 0,
            'saldo_gols': 0 })
    return 0  # sucesso


def atualizar_pontos(resultado: dict) -> int:
    gols_casa = resultado['gols_time1']
    gols_fora = resultado['gols_time2']
    encontrado = False

    for time in _tabela:
        if time['time'] == resultado['time1']:
            encontrado = True
            time['jogos']       += 1
            time['gols_pro']    += gols_casa
            time['gols_contra'] += gols_fora
            time['saldo_gols']   = time['gols_pro'] - time['gols_contra']
            if gols_casa > gols_fora:
                time['vitorias'] += 1
                time['pontos']   += 3
            elif gols_casa == gols_fora:
                time['empates']  += 1
                time['pontos']   += 1
            else:
                time['derrotas'] += 1
        elif time['time'] == resultado['time2']:
            encontrado = True
            time['jogos']       += 1
            time['gols_pro']    += gols_fora
            time['gols_contra'] += gols_casa
            time['saldo_gols']   = time['gols_pro'] - time['gols_contra']
            if gols_fora > gols_casa:
                time['vitorias'] += 1
                time['pontos']   += 3
            elif gols_fora == gols_casa:
                time['empates']  += 1
                time['pontos']   += 1
            else:
                time['derrotas'] += 1
    return 0 if encontrado else 1
   

def ordenar_classificacao():
    return sorted(_tabela,key=lambda t: (t['pontos'], t['vitorias'], t['saldo_gols'], t['gols_pro']),reverse=True)


def mostrar_classificacao() -> int:
    classificacao = ordenar_classificacao()
    if len(_tabela) == 0:
        return 1 
    cabecalho = f"{'Pos':<4} {'Time':<15} {'PTS':>4} {'J':>4} {'V':>4} {'E':>4} {'D':>4} {'GP':>4} {'GC':>4} {'SG':>4}"
    linhas = [cabecalho, '-' * len(cabecalho)]
    for pos, time in enumerate(classificacao, start=1):
        linhas.append(
            f"{pos:<4} {time['time']:<15} {time['pontos']:>4} {time['jogos']:>4} "
            f"{time['vitorias']:>4} {time['empates']:>4} {time['derrotas']:>4} "
            f"{time['gols_pro']:>4} {time['gols_contra']:>4} {time['saldo_gols']:>4}")
    print('\n'.join(linhas))
    return 0 